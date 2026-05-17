# Davomat Bot

Telegram attendance bot for a 10-person office. Tags workers at 8:30 AM (Tashkent time), classifies replies via Gemini AI, and posts a final report at 9:30 AM.

## Setup

```bash
pip3 install -r requirements.txt
cp .env.example .env  # fill in values
python3 bot.py
```

## Admin commands (private chat)

| Command | Description |
|---|---|
| `/workers` | List all active workers |
| `/addworker @username Name` | Add a worker |
| `/removeworker @username` | Deactivate a worker |
| `/report` | Today's attendance snapshot |
| `/override @username status` | Manually set a status |
| `/setmessage text` | Change the morning check-in message |
| `/export week` | Weekly report |
| `/export month` | Monthly report |

## Statuses

`present` · `coming_late` · `absent_permitted` · `absent_no_reason`
