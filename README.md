# Python Twitch bot

This is my experimental Python project. It works and if it's online, it can be tested on channel

https://www.twitch.tv/raccoonthetraveler

## Before running the application

1) Install Python v.3.7 or higher
2) Install PIPENV
3) When in project root directory, run the console command `pip install pipenv`
4) Create an account for your bot on Twitch.tv . I created a separate account, since I didn't figure out how to create multiple accounts linked to a single email.
5) Enable two factor authorization (required by Twitch) in bot account settings.

### **Configuring env.env file**

This file is essential while creating and launching the bot. Fill it with the following info

1) **TMI_TOKEN**. Follow the link https://twitchapps.com/tmi/ to receive the token. It will look like `oauth:symbolsaccdvgdfg`
2) **CLIENT_ID**. Register the app on Twitch.dev platform here `https://dev.twitch.tv/console/apps/create`. You may choose the domain name `localhost`, if you run the bot locally.
3) **BOT_NICK**. This is your bot twitch nickname. Notice: it will always be displayed in lower case, when posting messages in chat.
4) **BOT_PREFIX**. Leave it as it is
5) **CHANNEL**. This is the channel the bot will connect to. It always starts with `#` symbol, since Twitch uses IRC-client. Example: my nickname at the moment is Jeorgius_joke, so when I start the stream the channel name will be `#jeorgius_joke` 

## Troubleshoot

1) If you get “SSL: CERTIFICATE_VERIFY_FAILED” Error, use your path to Python home  and run the command in console `/Applications/Python\ 3.7/Install\ Certificates.command `
Reference:
https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error

## MurraySkull_bot

1) The bot responds to messages sent on chat. The list of such messages is available in JSON-format in `events/files/chat-events.json`
2) When one refers the bot (types `@MurraySkull_bot, <message>`), the bots responds with one of the reactions in JSON-file `events/files/answers.json`
3) There are commands that can be modified by moderators or by a streamer in file `events/files/commands.json` . To list available commands type `!commands` in chat. If you are a moderator and you need to modify the commands, type `!command help` to get the list of available actions
4) There is experimental feature to get the current weather. Example: `!weather Miami`
5) One can ask a Yes/No/Maybe question to the 8Ball. Example: `!8Ball am I a Rockstar?`
6) There is a small duel game based on Fallout VATS combat system. Type `!duel help` for the available commands. Notice: you'll need another player to start the game.