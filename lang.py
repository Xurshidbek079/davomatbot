LANGS = {
    "uz_lat": "O'zbek (lotin)",
    "uz_cyr": "Ўзбек (кирилл)",
    "ru": "Русский",
    "en": "English",
}

T = {
    "uz_lat": {
        "help_base": (
            "👨‍💼 Admin Panel\n\n"
            "Guruhlar:\n"
            "/groups — guruhlar ro'yxati\n"
            "/addgroup <chat_id> [Nomi] — guruhni o'zingizga biriktirish\n"
            "/removegroup <raqam> — guruhni o'chirish\n\n"
            "Xodimlar:\n"
            "/workers [guruh_raqami] — xodimlar ro'yxati\n"
            "/addworker @username [Ism] <guruh_raqami> — qo'shish\n"
            "/removeworker @username <guruh_raqami> — o'chirish\n\n"
            "Davomat:\n"
            "/askattendance [guruh_raqami] — HOZIR davomat so'rash (1 soat ochiq)\n"
            "/report [guruh_raqami] — bugungi holat\n"
            "/override @username <status> <guruh_raqami>\n"
            "  statuslar: present · absent_permitted · coming_late · absent_no_reason\n"
            "/export week|month [guruh_raqami] — hisobot\n\n"
            "Boshqa:\n"
            "/setmessage [matn] — kunlik xabarni o'zgartirish\n"
            "/setlang — tilni o'zgartirish\n"
            "/sendtest [guruh_raqami] — test xabar"
        ),
        "help_superadmin_extra": (
            "\n\n━━━ Superadmin ━━━\n"
            "/addadmin <user_id> [@username] — admin qo'shish\n"
            "/removeadmin <user_id> — adminni o'chirish\n"
            "/admins — barcha adminlar ro'yxati"
        ),
        "addadmin_usage": "Foydalanish: /addadmin <user_id> [@username]",
        "addadmin_ok": "✅ Admin qo'shildi: {label} (ID: {uid})",
        "removeadmin_usage": "Foydalanish: /removeadmin <user_id>",
        "removeadmin_ok": "✅ Admin o'chirildi: {uid}",
        "admins_empty": "Adminlar yo'q. /addadmin bilan qo'shing.",
        "admins_title": "👥 Adminlar:\n",
        "groups_empty": "Guruhlar yo'q.\nBotni guruhga qo'shing, keyin /addgroup <chat_id> bilan o'zingizga biriktiring.",
        "groups_title": "📋 Guruhlar:\n",
        "group_unnamed": "Nomsiz",
        "group_info": "{i}. {title}\n   ID: {chat_id} | {count} xodim",
        "group_info_owner": "{i}. {title}\n   ID: {chat_id} | {count} xodim\n   Owner: {owner}",
        "addgroup_usage": "Foydalanish: /addgroup <chat_id> [Nomi]",
        "addgroup_owned": "❌ Bu guruh boshqa admin tomonidan boshqariladi.",
        "addgroup_ok": "✅ Guruh biriktirildi: {title} ({chat_id})",
        "removegroup_ok": "✅ {title} o'chirildi",
        "group_not_found": "❌ Guruh topilmadi.",
        "workers_empty": "(xodim yo'q)",
        "addworker_usage": "Foydalanish: /addworker @username [Ism] <guruh_raqami>",
        "addworker_hint": "❌ Guruh topilmadi. /groups bilan raqamni tekshiring.",
        "addworker_ok": "✅ @{username} → {title}",
        "removeworker_usage": "Foydalanish: /removeworker @username <guruh_raqami>",
        "removeworker_ok": "✅ @{username} o'chirildi ({title})",
        "askatt_title": "Davomat so'rovi:\n",
        "askatt_no_workers": "⚠️ Xodim yo'q",
        "report_header": "📍 {title}\n📋 Davomat — {date}\n",
        "report_total": "\n📊 Jami: {count} ta xodim",
        "stat_present": "✅ Keldi",
        "stat_coming_late": "⏰ Kechikib keladi",
        "stat_absent_permitted": "🙏 Ruxsat bilan yo'q",
        "stat_absent_no_reason": "❌ Sababsiz yo'q",
        "stat_pending": "⏳ Kutilmoqda",
        "override_usage": "Foydalanish: /override @username {statuses} <guruh_raqami>",
        "override_ok": "✅ @{username} → {status} ({title})",
        "setmessage_usage": "Foydalanish: /setmessage [matn]",
        "setmessage_ok": "✅ Xabar yangilandi: \"{text}\"",
        "export_usage": "Foydalanish: /export week|month [guruh_raqami]",
        "export_week_label": "Haftalik ({from_date} - {to_date})",
        "export_month_label": "Oylik ({from_date} - {to_date})",
        "export_legend": "✅ keldi | ⏰ kech | 🙏 ruxsat | ❌ yo'q | — yo'q",
        "sendtest_ok": "✅ {title} ga yuborildi.",
        "sendtest_fail": "❌ {title}: {error}",
        "setlang_choose": "Tilni tanlang / Выберите язык / Choose language:",
        "setlang_ok": "✅ Til o'zgartirildi: {lang}",
        "report_title": "📋 Davomat hisoboti — {date}",
        "report_total_sched": "\n📊 Jami: {count} ta xodim",
        "label_present": "Keldi",
        "label_coming_late": "Kechikib keladi",
        "label_absent_permitted": "Ruxsat bilan yo'q",
        "label_absent_no_reason": "Sababsiz yo'q",
        "default_morning_msg": "Xodimlar, xayrli tong! ✋ Bugun ishda bormi? Iltimos, javob bering.",
    },

    "uz_cyr": {
        "help_base": (
            "👨‍💼 Админ Панел\n\n"
            "Гуруҳлар:\n"
            "/groups — гуруҳлар рўйхати\n"
            "/addgroup <chat_id> [Номи] — гуруҳни ўзингизга бириктириш\n"
            "/removegroup <рақам> — гуруҳни ўчириш\n\n"
            "Ходимлар:\n"
            "/workers [гуруҳ_рақами] — ходимлар рўйхати\n"
            "/addworker @username [Исм] <гуруҳ_рақами> — қўшиш\n"
            "/removeworker @username <гуруҳ_рақами> — ўчириш\n\n"
            "Давомат:\n"
            "/askattendance [гуруҳ_рақами] — ҲОЗИР давомат сўраш (1 соат очиқ)\n"
            "/report [гуруҳ_рақами] — бугунги ҳолат\n"
            "/override @username <статус> <гуруҳ_рақами>\n"
            "  статуслар: present · absent_permitted · coming_late · absent_no_reason\n"
            "/export week|month [гуруҳ_рақами] — ҳисобот\n\n"
            "Бошқа:\n"
            "/setmessage [матн] — кунлик хабарни ўзгартириш\n"
            "/setlang — тилни ўзгартириш\n"
            "/sendtest [гуруҳ_рақами] — тест хабар"
        ),
        "help_superadmin_extra": (
            "\n\n━━━ Суперадмин ━━━\n"
            "/addadmin <user_id> [@username] — админ қўшиш\n"
            "/removeadmin <user_id> — админни ўчириш\n"
            "/admins — барча админлар рўйхати"
        ),
        "addadmin_usage": "Фойдаланиш: /addadmin <user_id> [@username]",
        "addadmin_ok": "✅ Админ қўшилди: {label} (ID: {uid})",
        "removeadmin_usage": "Фойдаланиш: /removeadmin <user_id>",
        "removeadmin_ok": "✅ Админ ўчирилди: {uid}",
        "admins_empty": "Админлар йўқ. /addadmin билан қўшинг.",
        "admins_title": "👥 Админлар:\n",
        "groups_empty": "Гуруҳлар йўқ.\nБотни гуруҳга қўшинг, кейин /addgroup <chat_id> билан ўзингизга бириктиринг.",
        "groups_title": "📋 Гуруҳлар:\n",
        "group_unnamed": "Номсиз",
        "group_info": "{i}. {title}\n   ID: {chat_id} | {count} ходим",
        "group_info_owner": "{i}. {title}\n   ID: {chat_id} | {count} ходим\n   Owner: {owner}",
        "addgroup_usage": "Фойдаланиш: /addgroup <chat_id> [Номи]",
        "addgroup_owned": "❌ Бу гуруҳ бошқа админ томонидан бошқарилади.",
        "addgroup_ok": "✅ Гуруҳ бириктирилди: {title} ({chat_id})",
        "removegroup_ok": "✅ {title} ўчирилди",
        "group_not_found": "❌ Гуруҳ топилмади.",
        "workers_empty": "(ходим йўқ)",
        "addworker_usage": "Фойдаланиш: /addworker @username [Исм] <гуруҳ_рақами>",
        "addworker_hint": "❌ Гуруҳ топилмади. /groups билан рақамни текширинг.",
        "addworker_ok": "✅ @{username} → {title}",
        "removeworker_usage": "Фойдаланиш: /removeworker @username <гуруҳ_рақами>",
        "removeworker_ok": "✅ @{username} ўчирилди ({title})",
        "askatt_title": "Давомат сўрови:\n",
        "askatt_no_workers": "⚠️ Ходим йўқ",
        "report_header": "📍 {title}\n📋 Давомат — {date}\n",
        "report_total": "\n📊 Жами: {count} та ходим",
        "stat_present": "✅ Келди",
        "stat_coming_late": "⏰ Кечикиб келади",
        "stat_absent_permitted": "🙏 Рухсат билан йўқ",
        "stat_absent_no_reason": "❌ Сабабсиз йўқ",
        "stat_pending": "⏳ Кутилмоқда",
        "override_usage": "Фойдаланиш: /override @username {statuses} <гуруҳ_рақами>",
        "override_ok": "✅ @{username} → {status} ({title})",
        "setmessage_usage": "Фойдаланиш: /setmessage [матн]",
        "setmessage_ok": "✅ Хабар янгиланди: \"{text}\"",
        "export_usage": "Фойдаланиш: /export week|month [гуруҳ_рақами]",
        "export_week_label": "Ҳафталик ({from_date} - {to_date})",
        "export_month_label": "Ойлик ({from_date} - {to_date})",
        "export_legend": "✅ келди | ⏰ кеч | 🙏 рухсат | ❌ йўқ | — йўқ",
        "sendtest_ok": "✅ {title} га юборилди.",
        "sendtest_fail": "❌ {title}: {error}",
        "setlang_choose": "Тилни танланг / Выберите язык / Choose language:",
        "setlang_ok": "✅ Тил ўзгартирилди: {lang}",
        "report_title": "📋 Давомат ҳисоботи — {date}",
        "report_total_sched": "\n📊 Жами: {count} та ходим",
        "label_present": "Келди",
        "label_coming_late": "Кечикиб келади",
        "label_absent_permitted": "Рухсат билан йўқ",
        "label_absent_no_reason": "Сабабсиз йўқ",
        "default_morning_msg": "Ходимлар, хайрли тонг! ✋ Бугун ишда борми? Илтимос, жавоб беринг.",
    },

    "ru": {
        "help_base": (
            "👨‍💼 Панель администратора\n\n"
            "Группы:\n"
            "/groups — список групп\n"
            "/addgroup <chat_id> [Название] — привязать группу\n"
            "/removegroup <номер> — удалить группу\n\n"
            "Сотрудники:\n"
            "/workers [номер_группы] — список сотрудников\n"
            "/addworker @username [Имя] <номер_группы> — добавить\n"
            "/removeworker @username <номер_группы> — удалить\n\n"
            "Посещаемость:\n"
            "/askattendance [номер_группы] — запросить посещаемость СЕЙЧАС (открыто 1 час)\n"
            "/report [номер_группы] — сегодняшний статус\n"
            "/override @username <статус> <номер_группы>\n"
            "  статусы: present · absent_permitted · coming_late · absent_no_reason\n"
            "/export week|month [номер_группы] — отчёт\n\n"
            "Прочее:\n"
            "/setmessage [текст] — изменить ежедневное сообщение\n"
            "/setlang — изменить язык\n"
            "/sendtest [номер_группы] — тестовое сообщение"
        ),
        "help_superadmin_extra": (
            "\n\n━━━ Суперадмин ━━━\n"
            "/addadmin <user_id> [@username] — добавить администратора\n"
            "/removeadmin <user_id> — удалить администратора\n"
            "/admins — список всех администраторов"
        ),
        "addadmin_usage": "Использование: /addadmin <user_id> [@username]",
        "addadmin_ok": "✅ Администратор добавлен: {label} (ID: {uid})",
        "removeadmin_usage": "Использование: /removeadmin <user_id>",
        "removeadmin_ok": "✅ Администратор удалён: {uid}",
        "admins_empty": "Администраторов нет. Добавьте через /addadmin.",
        "admins_title": "👥 Администраторы:\n",
        "groups_empty": "Групп нет.\nДобавьте бота в группу, затем привяжите через /addgroup <chat_id>.",
        "groups_title": "📋 Группы:\n",
        "group_unnamed": "Без названия",
        "group_info": "{i}. {title}\n   ID: {chat_id} | {count} сотрудников",
        "group_info_owner": "{i}. {title}\n   ID: {chat_id} | {count} сотрудников\n   Owner: {owner}",
        "addgroup_usage": "Использование: /addgroup <chat_id> [Название]",
        "addgroup_owned": "❌ Эта группа уже управляется другим администратором.",
        "addgroup_ok": "✅ Группа привязана: {title} ({chat_id})",
        "removegroup_ok": "✅ {title} удалена",
        "group_not_found": "❌ Группа не найдена.",
        "workers_empty": "(нет сотрудников)",
        "addworker_usage": "Использование: /addworker @username [Имя] <номер_группы>",
        "addworker_hint": "❌ Группа не найдена. Проверьте номер через /groups.",
        "addworker_ok": "✅ @{username} → {title}",
        "removeworker_usage": "Использование: /removeworker @username <номер_группы>",
        "removeworker_ok": "✅ @{username} удалён ({title})",
        "askatt_title": "Запрос посещаемости:\n",
        "askatt_no_workers": "⚠️ Нет сотрудников",
        "report_header": "📍 {title}\n📋 Посещаемость — {date}\n",
        "report_total": "\n📊 Всего: {count} сотрудников",
        "stat_present": "✅ Присутствует",
        "stat_coming_late": "⏰ Опаздывает",
        "stat_absent_permitted": "🙏 Отсутствует (уважит.)",
        "stat_absent_no_reason": "❌ Отсутствует (без причины)",
        "stat_pending": "⏳ Ожидается",
        "override_usage": "Использование: /override @username {statuses} <номер_группы>",
        "override_ok": "✅ @{username} → {status} ({title})",
        "setmessage_usage": "Использование: /setmessage [текст]",
        "setmessage_ok": "✅ Сообщение обновлено: \"{text}\"",
        "export_usage": "Использование: /export week|month [номер_группы]",
        "export_week_label": "За неделю ({from_date} - {to_date})",
        "export_month_label": "За месяц ({from_date} - {to_date})",
        "export_legend": "✅ присутствует | ⏰ опоздание | 🙏 уважит. | ❌ нет | — нет данных",
        "sendtest_ok": "✅ Отправлено в {title}.",
        "sendtest_fail": "❌ {title}: {error}",
        "setlang_choose": "Тилни танланг / Выберите язык / Choose language:",
        "setlang_ok": "✅ Язык изменён: {lang}",
        "report_title": "📋 Отчёт по посещаемости — {date}",
        "report_total_sched": "\n📊 Всего: {count} сотрудников",
        "label_present": "Присутствует",
        "label_coming_late": "Опаздывает",
        "label_absent_permitted": "Отсутствует (уважит.)",
        "label_absent_no_reason": "Отсутствует (без причины)",
        "default_morning_msg": "Сотрудники, доброе утро! ✋ Вы на работе сегодня? Пожалуйста, ответьте.",
    },

    "en": {
        "help_base": (
            "👨‍💼 Admin Panel\n\n"
            "Groups:\n"
            "/groups — list groups\n"
            "/addgroup <chat_id> [Name] — link a group to yourself\n"
            "/removegroup <number> — remove a group\n\n"
            "Workers:\n"
            "/workers [group_number] — list workers\n"
            "/addworker @username [Name] <group_number> — add worker\n"
            "/removeworker @username <group_number> — remove worker\n\n"
            "Attendance:\n"
            "/askattendance [group_number] — request attendance NOW (open 1 hour)\n"
            "/report [group_number] — today's status\n"
            "/override @username <status> <group_number>\n"
            "  statuses: present · absent_permitted · coming_late · absent_no_reason\n"
            "/export week|month [group_number] — export report\n\n"
            "Other:\n"
            "/setmessage [text] — change daily check-in message\n"
            "/setlang — change language\n"
            "/sendtest [group_number] — send test message"
        ),
        "help_superadmin_extra": (
            "\n\n━━━ Superadmin ━━━\n"
            "/addadmin <user_id> [@username] — add admin\n"
            "/removeadmin <user_id> — remove admin\n"
            "/admins — list all admins"
        ),
        "addadmin_usage": "Usage: /addadmin <user_id> [@username]",
        "addadmin_ok": "✅ Admin added: {label} (ID: {uid})",
        "removeadmin_usage": "Usage: /removeadmin <user_id>",
        "removeadmin_ok": "✅ Admin removed: {uid}",
        "admins_empty": "No admins found. Add one with /addadmin.",
        "admins_title": "👥 Admins:\n",
        "groups_empty": "No groups found.\nAdd the bot to a group, then link it with /addgroup <chat_id>.",
        "groups_title": "📋 Groups:\n",
        "group_unnamed": "Unnamed",
        "group_info": "{i}. {title}\n   ID: {chat_id} | {count} workers",
        "group_info_owner": "{i}. {title}\n   ID: {chat_id} | {count} workers\n   Owner: {owner}",
        "addgroup_usage": "Usage: /addgroup <chat_id> [Name]",
        "addgroup_owned": "❌ This group is already managed by another admin.",
        "addgroup_ok": "✅ Group linked: {title} ({chat_id})",
        "removegroup_ok": "✅ {title} removed",
        "group_not_found": "❌ Group not found.",
        "workers_empty": "(no workers)",
        "addworker_usage": "Usage: /addworker @username [Name] <group_number>",
        "addworker_hint": "❌ Group not found. Check the number with /groups.",
        "addworker_ok": "✅ @{username} → {title}",
        "removeworker_usage": "Usage: /removeworker @username <group_number>",
        "removeworker_ok": "✅ @{username} removed ({title})",
        "askatt_title": "Attendance request:\n",
        "askatt_no_workers": "⚠️ No workers",
        "report_header": "📍 {title}\n📋 Attendance — {date}\n",
        "report_total": "\n📊 Total: {count} workers",
        "stat_present": "✅ Present",
        "stat_coming_late": "⏰ Coming late",
        "stat_absent_permitted": "🙏 Absent (permitted)",
        "stat_absent_no_reason": "❌ Absent (no reason)",
        "stat_pending": "⏳ Pending",
        "override_usage": "Usage: /override @username {statuses} <group_number>",
        "override_ok": "✅ @{username} → {status} ({title})",
        "setmessage_usage": "Usage: /setmessage [text]",
        "setmessage_ok": "✅ Message updated: \"{text}\"",
        "export_usage": "Usage: /export week|month [group_number]",
        "export_week_label": "Weekly ({from_date} - {to_date})",
        "export_month_label": "Monthly ({from_date} - {to_date})",
        "export_legend": "✅ present | ⏰ late | 🙏 permitted | ❌ absent | — no data",
        "sendtest_ok": "✅ Sent to {title}.",
        "sendtest_fail": "❌ {title}: {error}",
        "setlang_choose": "Тилни танланг / Выберите язык / Choose language:",
        "setlang_ok": "✅ Language changed: {lang}",
        "report_title": "📋 Attendance Report — {date}",
        "report_total_sched": "\n📊 Total: {count} workers",
        "label_present": "Present",
        "label_coming_late": "Coming late",
        "label_absent_permitted": "Absent (permitted)",
        "label_absent_no_reason": "Absent (no reason)",
        "default_morning_msg": "Team, good morning! ✋ Are you at work today? Please respond.",
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    text = T.get(lang, T["ru"]).get(key) or T["ru"].get(key, key)
    return text.format(**kwargs) if kwargs else text
