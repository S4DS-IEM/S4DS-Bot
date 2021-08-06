# S4DS-Bot

S4DS discord bot which serves for arXiv and Kaggle functionality.

This is a bot programmed entirely in python3 (Version 3.7+), primarily using discord.py (V 1.x(+) ), also known as the "Rewrite" version of discord.py.

Resources for discord.py : 

github - https://github.com/Rapptz/discord.py
Documentation - https://discordpy.readthedocs.io/en/stable/

-----------------------------------------------------------------------------

Setting up the bot : 

Step 1 : Login to discord on desktop.

Step 2 : Login to discord developer portal : 
            https://discord.com/developers/docs/intro

Step 3 : 
    3.1 : From the top menu (Under "DEVELOPER PORTAL") click on "Applications".

    3.2 : On the top right corner, click on "New Application". Assign a name to your application and finalize by clicking the "Create" button.

    3.3 : Now you will be directed to the application configuration page. Make sure your bot application is selected.

    3.4 : You can edit basic information in the default "General Information" tab.

    3.5 : Navigate to the third option "Bot" and under the "Build a Bot" section click the "Add Bot" and finalise your selection. (Note, this is irreversible for that application.)

    3.6 : Now, under the label "TOKEN", click "Copy" to copy the token and save it in "token.txt" in the directory "/src" of the code as it is the only valid key to control your bot using your code.

    3.7 : Check the following permissions : 
        i. PUBLIC BOT
        ii. REQUIRES OAUTH2 CODE GRANT
        iii. PRESENCE INTENT
        iv. SERVER MEMBERS INTENT

    3.8 : Now, go to the second option "OAuth2" and under label "SCOPES" select "bot".
          A new option "BOT PERMISSIONS" pops out where you can choose which permissions are checked when the bot is invited to a server.

          Copy the link generated under "SCOPES" and paste it in address box of browser.

---------------------------------------------------------------------------------

---------------------------------------------------------------------------------
Minor Fix 1 : Fixed Permissions for managing cogs

Now the load, unload and reload commands require administrator permissions for a user in order to use them, and flashes error message if they don't have necessary permissions.
This is implemented by using checks and handling errors.

---------------------------------------------------------------------------------

---------------------------------------------------------------------------------
Major Patch 1: Added arXiv functionality

arXiv search results powered by arXiv.org

<prefix> arxivshow <keyword> - Displays the top result using the searched keyword (including authors, title, summary, link and download link).

<prefix> arxivshowlud <keyword> - Displays top 5 papers using the searched keyword (including authors, title, link and download link) and sorts the result on the basis of last updated date.

<prefix> arxivshowr <keyword> - Displays top 5 papers using the searched keyword (including authors, title, link and download link) and sorts the result on the basis of relevance.

<prefix> arxivshowsd <keyword> - Displays top 5 papers using the searched keyword (including authors, title, link and download link) and sorts the result on the basis of submitted date. 

<prefix> arxivshowsumm <keyword> - Displays top 5 papers using the searched keyword (including authors, title, summary, link and download link).

---------------------------------------------------------------------------------

---------------------------------------------------------------------------------
Major Patch 2: Added Kaggle functionality

<prefix> list - Displays top 20 competitions from Kaggle Competition List

---------------------------------------------------------------------------------

So, following the above steps one can easily deploy the bot on a local machine.

Documentation for advanced and specific functions will be updated shortly.
