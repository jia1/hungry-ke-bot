# hungry-ke-bot
Flask service on Heroku for Telegram bot

Note: I use a remote Postgres database.

## Installation instructions for developers

### 1. In your local terminal (based on macOS 10.12.6)
```bash
brew install python3 # For Linux, "apt install python3", "yum install python3", or others depending on your distro.
git clone https://github.com/jia1/hungry-ke-bot.git
cd hungry-ke-bot
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt

# Run the following commands if the migrations directory is not available
python3 manage.py db init
python3 manage.py db migrate

# If you want to run a local server, you need to export the following enrivonment variables: BOT_TOKEN and DB_URL
# And then you run the following commands:
python3 manage.py db upgrade
```

### 2. On Heroku website or with Heroku CLI
1. Create a Heroku application.
1. Define the following environment variables: `BOT_TOKEN`, `DB_URL` (under the Settings tab).
1. Push repository and deploy to Heroku.
1. Switch on the `upgrade` dyno at `Configure dynos` (under the Resources tab).

### 3. Set up Telegram webhook
1. Access `https://api.telegram.org/bot(yourToken)/setWebhook` in your browser (replace yourToken with your bot token).
1. Access `https://api.telegram.org/bot(yourToken)/setWebhook?url=https://(someEndpoint)` in your browser (`someEndpoint` would be something like `https://my-heroku-app.herokuapp.com/get-todays-menu` depending on your Heroku app).

Refer to the following if still unsure: [how to use setwebhook in telegram? - Stackoverflow](https://stackoverflow.com/questions/36905455/how-to-use-setwebhook-in-telegram)

## Reset migration(s)
I am not sure what is the best way to do this, but this is how I do it:
1. Drop the `alembic` table
1. Delete the `migrations` directory
1. Re-run `python3 manage.py db init` and `python3 manage.py db migrate`
1. Push changes

## Uploading CSV file data to Postgres database

### 1. Prepare the csv file
- Please follow the format in `menu.csv.sample`.
- Date to follow this format `dd/mm/yyyy`. E.g. `12/1/2018` for January 12, 2018 and `25/12/2018` for December 25, 2018.
- All characters to be of lower case. The bot will capitalize each word/phrase.
- Be extra careful about the format to specify multiple dishes. Refer to the CSV file.

### 2. Running the upload script in the terminal
1. Download the script via `git clone` or a simple `Save As`.
1. Put `menu.csv` into the same directory for simplicity.

Assuming `upload.py` and `menu.csv` are in the current directory, run the following commands:
```bash
pip3 install psycopg2
export DB_URL=(yourDatabaseUrl) # For Windows, you must configure this via "Edit environment variables in your account"
python upload.py menu.csv
```
You should observe the rows in your CSV file being printed to the terminal.
