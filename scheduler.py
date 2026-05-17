import os
import logging
from datetime import date, datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from database import (get_active_groups, get_active_workers, get_setting,
                      mark_attendance, get_unresponded, get_today_attendance)
from lang import t

load_dotenv()
TZ = pytz.timezone("Asia/Tashkent")
ADMIN_ID = int(os.getenv("ADMIN_TELEGRAM_ID", "0"))
logger = logging.getLogger(__name__)

EMOJI = {"present": "✅", "coming_late": "⏰", "absent_permitted": "🙏", "absent_no_reason": "❌"}

def build_report(group_chat_id, date_str, attendance, title=None, lang="uz_lat"):
    d = datetime.strptime(date_str, "%Y-%m-%d")
    LABEL = {
        "present": t("label_present", lang),
        "coming_late": t("label_coming_late", lang),
        "absent_permitted": t("label_absent_permitted", lang),
        "absent_no_reason": t("label_absent_no_reason", lang),
    }
    grps = {k: [] for k in LABEL}
    for u, s in attendance.items():
        grps.get(s, grps["absent_no_reason"]).append(u)
    prefix = f"📍 {title}\n" if title else ""
    lines = [f"{prefix}{t('report_title', lang, date=d.strftime('%d.%m.%Y'))}\n"]
    for key, label in LABEL.items():
        if grps[key]:
            lines.append(f"{EMOJI[key]} {label} ({len(grps[key])}):")
            lines += [f"• @{u}" for u in grps[key]]
    lines.append(t("report_total_sched", lang, count=sum(len(v) for v in grps.values())))
    return "\n".join(lines)

async def send_attendance_request(app, group):
    """Send attendance check-in message and open a 1-hour reply window."""
    workers = get_active_workers(group["chat_id"])
    if not workers:
        return False
    msg = get_setting("daily_message") or t("default_morning_msg")
    tags = " ".join(f"@{w}" for w in workers)
    await app.bot.send_message(chat_id=int(group["chat_id"]), text=f"{msg}\n\n{tags}")
    app.bot_data.setdefault("sessions", {})[group["chat_id"]] = datetime.now(TZ) + timedelta(hours=1)
    return True

async def morning_job(app):
    for group in get_active_groups():
        try:
            await send_attendance_request(app, group)
        except Exception as e:
            logger.error(f"morning_job {group['chat_id']}: {e}")

async def closing_job(app):
    today = date.today().isoformat()
    app.bot_data["sessions"] = {}
    for group in get_active_groups():
        try:
            for w in get_unresponded(group["chat_id"], today):
                mark_attendance(w, group["chat_id"], today, "absent_no_reason")
            workers = get_active_workers(group["chat_id"])
            att = get_today_attendance(group["chat_id"], today)
            report = build_report(group["chat_id"], today,
                                  {w: att.get(w, "absent_no_reason") for w in workers},
                                  group.get("title"))
            await app.bot.send_message(chat_id=int(group["chat_id"]), text=report)
            await app.bot.send_message(chat_id=ADMIN_ID, text=report)
        except Exception as e:
            logger.error(f"closing_job {group['chat_id']}: {e}")

def setup_scheduler(app):
    scheduler = AsyncIOScheduler(timezone=TZ)
    scheduler.add_job(morning_job, "cron", day_of_week="mon-fri", hour=8, minute=30, args=[app])
    scheduler.add_job(closing_job, "cron", day_of_week="mon-fri", hour=9, minute=30, args=[app])
    scheduler.start()
