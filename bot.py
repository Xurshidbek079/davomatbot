import os
import logging
from datetime import date, timedelta, datetime
import pytz
from telegram import Update, ReactionTypeEmoji, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv
from database import (init_db, add_admin, remove_admin, get_admins, is_registered_admin,
                      add_group, remove_group, get_active_groups, get_group_by_num, get_group,
                      add_worker, remove_worker, get_active_workers, save_user_id,
                      mark_attendance, get_today_attendance, get_attendance_range,
                      get_setting, set_setting, get_user_lang, set_user_lang)
from gemini import classify_response
from scheduler import build_report, send_attendance_request, setup_scheduler
from lang import t, LANGS

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPERADMIN_ID = os.getenv("ADMIN_TELEGRAM_ID")
TZ = pytz.timezone("Asia/Tashkent")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def is_superadmin(uid): return str(uid) == SUPERADMIN_ID
def is_any_admin(uid): return is_superadmin(uid) or is_registered_admin(uid)
def owner_filter(uid): return None if is_superadmin(uid) else str(uid)
def ulang(uid): return get_user_lang(uid)

def resolve_group(args, uid, idx=0):
    """Resolve a group by positional number or raw chat_id, scoped to caller's ownership."""
    oid = owner_filter(uid)
    if not args or len(args) <= (idx if idx >= 0 else len(args) + idx): return None
    try:
        val = int(args[idx])
        if val < 0:
            return next((g for g in get_active_groups(oid) if g["chat_id"] == str(val)), None)
        return get_group_by_num(val, oid)
    except (ValueError, IndexError):
        return None

def caller_groups(uid):
    return get_active_groups(owner_filter(uid))

def _lang_keyboard(prefix: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇿 O'zbek (lotin)", callback_data=f"{prefix}:uz_lat"),
            InlineKeyboardButton("🇺🇿 Ўзбек (кирилл)", callback_data=f"{prefix}:uz_cyr"),
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data=f"{prefix}:ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data=f"{prefix}:en"),
        ],
    ])

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    await u.message.reply_text(
        t("setlang_choose"),
        reply_markup=_lang_keyboard("startlang")
    )

async def startlang_callback(u: Update, c: ContextTypes.DEFAULT_TYPE):
    query = u.callback_query
    await query.answer()
    if not is_any_admin(u.effective_user.id): return
    lang_code = query.data.split(":")[1]
    if lang_code not in LANGS: return
    set_user_lang(u.effective_user.id, lang_code)
    uid = u.effective_user.id
    extra = t("help_superadmin_extra", lang_code) if is_superadmin(uid) else ""
    await query.edit_message_text(t("help_base", lang_code) + extra)

# ── Superadmin: admin management ──────────────────────────────────────────────

async def addadmin_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_superadmin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    if not c.args:
        await u.message.reply_text(t("addadmin_usage", lang)); return
    uid_arg = c.args[0]
    username = c.args[1].lstrip("@") if len(c.args) > 1 else None
    add_admin(uid_arg, username, added_by=SUPERADMIN_ID)
    label = f"@{username}" if username else uid_arg
    await u.message.reply_text(t("addadmin_ok", lang, label=label, uid=uid_arg))

async def removeadmin_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_superadmin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    if not c.args:
        await u.message.reply_text(t("removeadmin_usage", lang)); return
    remove_admin(c.args[0])
    await u.message.reply_text(t("removeadmin_ok", lang, uid=c.args[0]))

async def admins_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_superadmin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    admins = get_admins()
    if not admins:
        await u.message.reply_text(t("admins_empty", lang)); return
    lines = [t("admins_title", lang)]
    for i, a in enumerate(admins, 1):
        name = f"@{a['username']}" if a.get("username") else a["telegram_user_id"]
        lines.append(f"{i}. {name} (ID: {a['telegram_user_id']})")
    await u.message.reply_text("\n".join(lines))

# ── Group management ───────────────────────────────────────────────────────────

async def groups_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    uid = u.effective_user.id
    lang = ulang(uid)
    groups = caller_groups(uid)
    if not groups:
        await u.message.reply_text(t("groups_empty", lang)); return
    lines = [t("groups_title", lang)]
    for i, g in enumerate(groups, 1):
        count = len(get_active_workers(g["chat_id"]))
        title = g["title"] or t("group_unnamed", lang)
        if is_superadmin(uid):
            lines.append(t("group_info_owner", lang, i=i, title=title,
                           chat_id=g["chat_id"], count=count, owner=g["owner_id"] or "—"))
        else:
            lines.append(t("group_info", lang, i=i, title=title,
                           chat_id=g["chat_id"], count=count))
    await u.message.reply_text("\n".join(lines))

async def addgroup_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    if not c.args:
        await u.message.reply_text(t("addgroup_usage", lang)); return
    uid = u.effective_user.id
    chat_id, title = c.args[0], " ".join(c.args[1:]) or None
    existing = get_group(chat_id)
    if (existing and existing.get("owner_id") and
            existing["owner_id"] != str(uid) and not is_superadmin(uid)):
        await u.message.reply_text(t("addgroup_owned", lang)); return
    add_group(chat_id, title, owner_id=str(uid))
    await u.message.reply_text(t("addgroup_ok", lang, title=title or chat_id, chat_id=chat_id))

async def removegroup_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    group = resolve_group(c.args, u.effective_user.id)
    if not group:
        await u.message.reply_text(t("group_not_found", lang)); return
    remove_group(group["chat_id"])
    title = group["title"] or t("group_unnamed", lang)
    await u.message.reply_text(t("removegroup_ok", lang, title=title))

# ── Worker management ──────────────────────────────────────────────────────────

async def workers_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    uid = u.effective_user.id
    lang = ulang(uid)
    groups = ([resolve_group(c.args, uid)] if c.args else caller_groups(uid))
    groups = [g for g in groups if g]
    if not groups:
        await u.message.reply_text(t("group_not_found", lang)); return
    lines = []
    for g in groups:
        ws = get_active_workers(g["chat_id"])
        lines.append(f"📍 {g['title'] or g['chat_id']}:")
        lines += ([f"  {i+1}. @{w}" for i, w in enumerate(ws)] if ws else [f"  {t('workers_empty', lang)}"])
    await u.message.reply_text("\n".join(lines))

async def addworker_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    if len(c.args) < 2:
        await u.message.reply_text(t("addworker_usage", lang)); return
    uid = u.effective_user.id
    group = resolve_group(c.args, uid, -1)
    if not group:
        await u.message.reply_text(t("addworker_hint", lang)); return
    username = c.args[0].lstrip("@")
    full_name = " ".join(c.args[1:-1]) or None
    add_worker(username, group["chat_id"], full_name)
    title = group["title"] or group["chat_id"]
    await u.message.reply_text(t("addworker_ok", lang, username=username, title=title))

async def removeworker_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    if len(c.args) < 2:
        await u.message.reply_text(t("removeworker_usage", lang)); return
    uid = u.effective_user.id
    group = resolve_group(c.args, uid, 1)
    if not group:
        await u.message.reply_text(t("group_not_found", lang)); return
    username = c.args[0].lstrip("@")
    remove_worker(username, group["chat_id"])
    title = group["title"] or group["chat_id"]
    await u.message.reply_text(t("removeworker_ok", lang, username=username, title=title))

# ── Attendance ─────────────────────────────────────────────────────────────────

async def askattendance_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    uid = u.effective_user.id
    lang = ulang(uid)
    groups = ([resolve_group(c.args, uid)] if c.args else caller_groups(uid))
    groups = [g for g in groups if g]
    if not groups:
        await u.message.reply_text(t("group_not_found", lang)); return
    results = []
    for g in groups:
        try:
            sent = await send_attendance_request(c.application, g)
            icon = "✅" if sent else t("askatt_no_workers", lang)
            results.append(f"{icon} — {g['title'] or g['chat_id']}")
        except Exception as e:
            results.append(f"❌ {g['title'] or g['chat_id']}: {e}")
    await u.message.reply_text(t("askatt_title", lang) + "\n".join(results))

async def report_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    uid = u.effective_user.id
    lang = ulang(uid)
    groups = ([resolve_group(c.args, uid)] if c.args else caller_groups(uid))
    groups = [g for g in groups if g]
    if not groups:
        await u.message.reply_text(t("group_not_found", lang)); return
    today, now_str = date.today().isoformat(), datetime.now(TZ).strftime("%d.%m.%Y")
    STAT = {
        "present": t("stat_present", lang),
        "coming_late": t("stat_coming_late", lang),
        "absent_permitted": t("stat_absent_permitted", lang),
        "absent_no_reason": t("stat_absent_no_reason", lang),
        "pending": t("stat_pending", lang),
    }
    for g in groups:
        ws = get_active_workers(g["chat_id"])
        att = get_today_attendance(g["chat_id"], today)
        buckets = {k: [] for k in STAT}
        for w in ws: buckets[att.get(w, "pending")].append(w)
        title = g["title"] or g["chat_id"]
        lines = [t("report_header", lang, title=title, date=now_str)]
        for key, label in STAT.items():
            if buckets[key]:
                lines.append(f"{label} ({len(buckets[key])}):")
                lines += [f"• @{w}" for w in buckets[key]]
        lines.append(t("report_total", lang, count=len(ws)))
        await u.message.reply_text("\n".join(lines))

async def override_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    valid = ["present", "absent_no_reason", "absent_permitted", "coming_late"]
    if len(c.args) < 3 or c.args[1] not in valid:
        await u.message.reply_text(t("override_usage", lang, statuses="|".join(valid))); return
    uid = u.effective_user.id
    group = resolve_group(c.args, uid, 2)
    if not group:
        await u.message.reply_text(t("group_not_found", lang)); return
    username = c.args[0].lstrip("@")
    mark_attendance(username, group["chat_id"], date.today().isoformat(), c.args[1])
    title = group["title"] or group["chat_id"]
    await u.message.reply_text(t("override_ok", lang, username=username, status=c.args[1], title=title))

async def setmessage_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    text = " ".join(c.args)
    if not text:
        await u.message.reply_text(t("setmessage_usage", lang)); return
    set_setting("daily_message", text)
    await u.message.reply_text(t("setmessage_ok", lang, text=text))

async def export_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    if not c.args:
        await u.message.reply_text(t("export_usage", lang)); return
    uid, period, today = u.effective_user.id, c.args[0], date.today()
    if period == "week":
        from_date = today - timedelta(days=today.weekday())
        label = t("export_week_label", lang,
                  from_date=from_date.strftime("%d.%m"), to_date=today.strftime("%d.%m.%Y"))
    elif period == "month":
        from_date = today.replace(day=1)
        label = t("export_month_label", lang,
                  from_date=from_date.strftime("%d.%m"), to_date=today.strftime("%d.%m.%Y"))
    else:
        await u.message.reply_text(t("export_usage", lang)); return
    groups = ([resolve_group(c.args, uid, 1)] if len(c.args) > 1 else caller_groups(uid))
    groups = [g for g in groups if g]
    dates = [from_date + timedelta(days=i) for i in range((today - from_date).days + 1)
             if (from_date + timedelta(days=i)).weekday() < 5]
    em = {"present": "✅", "coming_late": "⏰", "absent_permitted": "🙏", "absent_no_reason": "❌"}
    for g in groups:
        records = get_attendance_range(g["chat_id"], from_date.isoformat(), today.isoformat())
        ws = get_active_workers(g["chat_id"])
        lines = [f"📍 {g['title'] or g['chat_id']} — {label}", ""]
        for w in ws:
            row = "".join(em.get(records.get((w, d.isoformat())), "—") for d in dates)
            lines.append(f"@{w}: {row}")
        lines.append(f"\n{t('export_legend', lang)}")
        await u.message.reply_text("\n".join(lines))

async def sendtest_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    uid = u.effective_user.id
    lang = ulang(uid)
    groups = ([resolve_group(c.args, uid)] if c.args else caller_groups(uid))
    groups = [g for g in groups if g]
    if not groups:
        await u.message.reply_text(t("group_not_found", lang)); return
    for g in groups:
        title = g["title"] or g["chat_id"]
        try:
            await c.bot.send_message(chat_id=int(g["chat_id"]), text=f"✅ Test — {title}")
            await u.message.reply_text(t("sendtest_ok", lang, title=title))
        except Exception as e:
            await u.message.reply_text(t("sendtest_fail", lang, title=title, error=e))

# ── Language selection ─────────────────────────────────────────────────────────

async def setlang_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_chat.type != "private" or not is_any_admin(u.effective_user.id): return
    lang = ulang(u.effective_user.id)
    await u.message.reply_text(t("setlang_choose", lang),
                                reply_markup=_lang_keyboard("setlang"))

async def setlang_callback(u: Update, c: ContextTypes.DEFAULT_TYPE):
    query = u.callback_query
    await query.answer()
    if not is_any_admin(u.effective_user.id): return
    lang_code = query.data.split(":")[1]
    if lang_code not in LANGS: return
    set_user_lang(u.effective_user.id, lang_code)
    await query.edit_message_text(t("setlang_ok", lang_code, lang=LANGS[lang_code]))

# ── Group message handling ─────────────────────────────────────────────────────

REACTION = {"present": "✅", "coming_late": "⏰", "absent_permitted": "🙏", "absent_no_reason": "❌"}

async def any_message(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not u.effective_chat: return
    chat = u.effective_chat
    if chat.type in ("group", "supergroup"):
        add_group(str(chat.id), chat.title)  # auto-register, never overwrites owner
        logger.info(f"GROUP | id={chat.id} title={chat.title} "
                    f"user=@{getattr(u.effective_user, 'username', '?')} "
                    f"text={u.message.text[:60] if u.message and u.message.text else '(no text)'}")

async def group_message(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not u.message or not u.message.text or not u.effective_user: return
    user = u.effective_user
    username = (user.username or "").lower()
    gid = str(u.effective_chat.id)
    workers = [w.lower() for w in get_active_workers(gid)]
    if username in workers:
        save_user_id(username, user.id, gid)
    now = datetime.now(TZ)
    in_schedule = (now.replace(hour=8, minute=30, second=0, microsecond=0) <= now <=
                   now.replace(hour=9, minute=30, second=0, microsecond=0))
    sessions = c.bot_data.get("sessions", {})
    in_session = gid in sessions and now < sessions[gid]
    if not (in_schedule or in_session) or username not in workers: return
    today = now.date().isoformat()
    if username in get_today_attendance(gid, today): return
    status = classify_response(u.message.text)
    mark_attendance(username, gid, today, status, u.message.text)
    try:
        await c.bot.set_message_reaction(
            chat_id=u.effective_chat.id,
            message_id=u.message.message_id,
            reaction=[ReactionTypeEmoji(emoji=REACTION[status])]
        )
    except Exception:
        pass

async def post_init(app):
    env_group = os.getenv("TELEGRAM_GROUP_ID")
    if env_group:
        add_group(env_group, owner_id=SUPERADMIN_ID)
    setup_scheduler(app)

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    for cmd, fn in [
        (["start", "help"], start),
        ("addadmin", addadmin_cmd), ("removeadmin", removeadmin_cmd), ("admins", admins_cmd),
        ("groups", groups_cmd), ("addgroup", addgroup_cmd), ("removegroup", removegroup_cmd),
        ("workers", workers_cmd), ("addworker", addworker_cmd), ("removeworker", removeworker_cmd),
        ("askattendance", askattendance_cmd), ("report", report_cmd), ("override", override_cmd),
        ("setmessage", setmessage_cmd), ("setlang", setlang_cmd),
        ("export", export_cmd), ("sendtest", sendtest_cmd),
    ]:
        app.add_handler(CommandHandler(cmd, fn))
    app.add_handler(CallbackQueryHandler(startlang_callback, pattern="^startlang:"))
    app.add_handler(CallbackQueryHandler(setlang_callback, pattern="^setlang:"))
    app.add_handler(MessageHandler(filters.ALL, any_message), group=-1)
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, group_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
