<div align="center">
  <br />
  <p>
    <a href="https://owaspvit.org"><img src="https://i.imgur.com/6Zc3DVq.png" width="500" alt="owaspvit.org" /></a>
  </p>
  <br />
  <p>
    <a href="https://discord.gg/aMgWPApkyS"><img src="https://img.shields.io/discord/738109119671566447?color=5865F2&logo=discord&logoColor=white" alt="Discord server" /></a>
    <a href="https://github.com/owaspvit/owaspvit.org"><img src="https://github.com/owaspvit/owaspvit.org/actions/workflows/dependency-check.yml/badge.svg" alt="Python Requirements Test" /></a>
    <a href="https://owaspvit.org"><img src="https://img.shields.io/website/https/owaspvit.org" alt="Website status" /></a>
    <a href="https://github.com/owaspvit/owaspvit.org/blob/main/LICENSE"><img src="https://img.shields.io/github/license/owaspvit/owaspvit.org" alt="LICENSE" /></a>
    <a href="https://github.com/owaspvit/owaspvit.org"><img src="https://img.shields.io/github/languages/count/owaspvit/owaspvit.org" alt="Language count" /></a>
    <a href="https://github.com/owaspvit/owaspvit.org/issues"><img src="https://camo.githubusercontent.com/f5054ffcd4245c10d3ec85ef059e07aacf787b560f83ad4aec2236364437d097/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f6e747269627574696f6e732d77656c636f6d652d627269676874677265656e2e7376673f7374796c653d666c6174" alt="Contributions" /></a>
  </p>
</div>

## About

[owaspvit.org](https://owaspvit.org) is the official Open Source initiative by the OWASP Student Chapter at VIT Chennai. It comprises two modules: A web application and a discord bot.
These modules provide a wide range of functionalities for managing the chapter members.

- Leaderboard for contribution tracking integrated with the discord bot
- Digital Certificate locker integrated with the discord bot
- Projects showcase integrated with the discord bot
- CTF event management integrated with the discord bot
- Gaming event management

### Requirements

- [docker and docker-compose](https://www.docker.com/products/docker-desktop)
- [Firebase Realtime Database JSON SDK](https://firebase.google.com/docs/database)
- [MongoDB Connection String](https://docs.mongodb.com/manual/reference/connection-string/)
- [Google Sheets JSON SDK and Sheet ID](https://developers.google.com/sheets/api)
- [GitHub API Key](https://github.com/settings/tokens)
- [Discord Bot Token](https://discord.com/developers/applications)
- [Discord target channel ID](https://www.remote.tools/remote-work/how-to-find-discord-id)

## Setup

Open `terminal` and execute:
```shell
git clone https://github.com/owaspvit/owaspvit.org.git
cd owaspvit.org
```

Create `config.toml`:
```toml
# Keys
title = "owaspvit.org configuration"

# Web app configuration
[app]
secret = "your_web_app_secret"
github = "your_github_api_key"

# Database Configuration
[database]
mongoURI = "your_mongodb_connection_string"
firebaseDB = "your_firebase_db_url"
firebaseStorage = "your_firebase_storage_url"

# Bot configuration
[bot]
token = "your_discord_bot_token"
sheet = "your_google_sheet_id"
channel = discord_target_channel_id

# OWASP VITCC CTF Configuration
[ctf]
apiKey = "your_firebase_api_key"
authDomain = "your_firebase_auth_domain"
databaseURL = "your_firebase_db_url"
projectId = "your_firebase_project_id"
storageBucket = "your_firebase_storage_bucket_url"
messagingSenderId = "your_firebase_messaging_sender_id"
appId = "your_firebase_app_id"
measurementId = "your_firebase_measurement_id"
```
- Rename the downloaded *Firebase Realtime Database JSON SDK* to `firebase.json`
- Rename the downloaded *Google Sheets JSON SDK* to `keys.json`
- Now copy the `config.toml`, `firebase.json` and `keys.json` to both the `web` and `bot` folders.

## Starting up

Open `terminal` in the `owaspvit.org` project directory and execute the following:
```shell
docker-compose up
```

## Stopping

Open `terminal` in the `owaspvit.org` project directory and execute the following:
```shell
docker-compose down
```

## Discord Bot Information

You can view the OWASP VITCC Bot commands by executing `!owasp help`

## Links

- [Website](https://owaspvit.org)
- [Leaderboard](https://owaspvit.org/leaderboard)
- [Certificate Locker](https://owaspvit.org/locker)
- [Projects Showcase](https://owaspvit.org/projects)
- [CTF Event Management](https://owaspvit.org/ctf)
- [Gaming Event Management](https://owaspvit.org/valowasp)

## Contributing

Before creating an issue, please ensure that it hasn't already been reported/suggested.

The issue tracker is only for bug reports and enhancement suggestions. If you have a question, please ask it in the [Discord server](https://discord.gg/aMgWPApkyS) instead of opening an issue – you will get redirected there anyway.

If you wish to contribute to the owaspvit.org codebase or documentation, feel free to fork the repository and submit a pull request.

## Help

If you don't understand something in the documentation, you are experiencing problems, or you just need a gentle
nudge in the right direction, please don't hesitate to join our [Discord Server](https://discord.gg/aMgWPApkyS).
