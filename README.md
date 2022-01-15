# S4DS-Bot

S4DS discord bot which primarily serves for arXiv, kaggle and educational memes (using reddit) functionality.

This is a bot programmed entirely in python3 (Version 3.7+), primarily using discord.py (V 1.x(+) ), also known as the "Rewrite" version of discord.py.

Resources for discord.py : 

github - https://github.com/Rapptz/discord.py
Documentation - https://discordpy.readthedocs.io/en/stable/

 - All dependencies listed in `requirements.txt`

-----------------------------------------------------------------------------

## Setting up the bot : 

Step 1 : Login to discord on desktop.

Step 2 : Login to discord developer portal : 
            https://discord.com/developers/docs/intro

Step 3 : 
    3.1 : From the top menu (Under "DEVELOPER PORTAL") click on "Applications".

    3.2 : On the top right corner, click on "New Application". Assign a name to your application and finalize by clicking the "Create" button.

    3.3 : Now you will be directed to the application configuration page. Make sure your bot application is selected.

    3.4 : You can edit basic information in the default "General Information" tab.

    3.5 : Navigate to the third option "Bot" and under the "Build a Bot" section click the "Add Bot" and finalise your selection. (Note, this is irreversible for that application.)

    3.6 : Now, under the label "TOKEN", click "Copy" to copy the token and save it as the environment variable, `DISCORD-TOKEN`. 

    3.7 : Check the following permissions : 
        i. PUBLIC BOT
        ii. REQUIRES OAUTH2 CODE GRANT
        iii. PRESENCE INTENT
        iv. SERVER MEMBERS INTENT
        v. MESSAGE CONTENT INTENT (To Be Enforced w.e.f 30th April, 2022)

    3.8 : Now, go to the second option "OAuth2" and under label "SCOPES" select "bot".
          A new option "BOT PERMISSIONS" pops out where you can choose which permissions are checked when the bot is invited to a server.

          Copy the URL generated under "SCOPES" and paste it in address box of browser, and complete the OAuth2 Process.

---------------------------------------------------------------------------------

---------------------------------------------------------------------------------

## Environment Variables / Config Vars : 

The application/bot has the portability of being deployed either locally or to the cloud, ensured through a collection of environment variables, which also deal with other aspects such as database of choice, API tokens, credentials, etc.

 - `DISCORD_TOKEN` : Unique API Token for authenticating the bot's client with discord API.

 - `KAGGLE_USERNAME` : Username of kaggle user whose account has been used to issue API token.

 - `KAGGLE_KEY` : Unique API Token for interacting with kaggle's api.

 - `REDDIT_CREDENTIALS` : Credentials for interacting with reddit's api in `json` format.

 - `PREFIXES_TABLE` : Table storing _unique_ prefixes for each server.

 - `SUBREDDITS_TABLE` : Table storing list of _unique_ subreddits for each server.

 - `AUTOPOST_TABLE` : Table storing `channel_id`s of servers enabling autopost. 

 - `CURRENT_ENVIRONMENT` : Specify `local` if deployed locally, any other string for otherwise. 
    - If `CURRENT_ENVIRONMENT` set to `local`, set the following environment variables : 
        - `DATABASE_NAME` : Name of local PostgreSQL Database.
        - `DATABASE_USER` : Name of the database role used for authentication.
        - `DATABASE_PASSWORD` : Password to be used for authentication.
    - If `CURRENT_ENVIRONMENT` is set to something else, set the follwoing environment variable : 
        -  `DATABASE_URL` : Connection arguments specified using as a single string in the [libpq connection URI format](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) : `postgres://user:password@host:port/database?option=value`. Typically, for cloud platforms like heroku, this is auto-configured and as such, shouldnot be tampered with. 

### Note : 
 - Modify credentials / code accordingly case of any change in use of preferred database.
 - Changes are logged only during uptime.
---------------------------------------------------------------------------------

So, following the above steps one can easily deploy the bot on a local machine or as a web application hosted on a cloud platform.

