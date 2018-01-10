# hungry-ke-bot
Flask service on Heroku for Telegram bot

Note: I use a remote Postgres database.

### Installation instructions (based on macOS 10.12.6)
```bash
brew install python3
git clone https://github.com/jia1/hungry-ke-bot.git
cd hungry-ke-bot
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
python3 manage.py db init
python3 manage.py db migrate
```

### On Heroku website or with Heroku CLI
1. Define the following environment variables: `BOT_TOKEN`, `DB_URL` (under the Settings tab)
1. Switch on the `upgrade` dyno at `Configure dynos` (under the Resources tab)
1. Deploy
