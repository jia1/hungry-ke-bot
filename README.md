# hungry-ke-bot
Flask service on Heroku for Telegram bot

## Instructions for users

### Uploading CSV file data to Postgres database

#### 1. Prepare the csv file
- Please follow the format in `menu.csv.sample`.
- The date must follow this format `dd/mm/yyyy`. E.g. `12/1/2018` for January 12, 2018 and `25/12/2018` for December 25, 2018.
- All characters can be of lower case. The bot will capitalize each column entry.
- Be extra careful about the format to specify multiple dishes. Refer to the CSV file.

#### 2. Running the upload script in the terminal
1. Download the script via `git clone` or a simple `Save As`.
1. Put `menu.csv` into the same directory for simplicity.
1. Install Python 3 (comes with `pip`).

Assuming `upload.py` and `menu.csv` are in the current directory, run the following commands:

##### macOS or Linux
```bash
pip3 install psycopg2
export DB_URL=(yourDatabaseUrl)
python3 upload.py menu.csv
```

##### Windows

Scroll down further to see the screenshots.

Instructions:
1. Install Python 3.6.4
1. Press the Windows icon on your keyboard to search Windows
1. Type "environment" in the search field
1. Go to "Edit environment variables for your account"
1. Click "New" under "User variables for (yourUsername)"
1. Set "Variable name" to "DB_URL" and "Variable value" to (yourDatabaseUrl)
1. Open a new command prompt window and run the following commands:

```cmd
cd Documents\hungry-ke-bot # Or wherever this folder is inside your computer
pip install psycopg2
python upload.py menu.csv
```

You should observe the rows in your CSV file being printed to the terminal.

### Updating or deleting

Please delete from the database manually (i.e. `DELETE FROM menu_items`) and do the upload procedure with the updated CSV file.

## Installation instructions for developers

### 1. In your local terminal (based on macOS 10.12.6)
```bash
brew install python3 # Linux has different package managers (e.g. apt, yum)
git clone https://github.com/jia1/hungry-ke-bot.git
cd hungry-ke-bot
python3 -m venv .
. bin/activate
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
