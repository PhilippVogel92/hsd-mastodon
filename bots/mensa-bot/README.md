# HSD Mensa Bot for Mastodon

## Fetches the mensa food for the current day and posts it on mastodon.

You need to create a `.env` file inside this folder with environment variables. Following is a list with examples of all needed parameters.
| Name | Description | Values |
|---|---|---|
| MASTODON_URL | Url of the Mastodon-Server on which the Toots should be posted | https://mastodon.social/ |
| MENSA_BOT_ACCESS_TOKEN | Access token of the mastodon application | 1a2s3d4f5_6g7h8j9 |
| MENSA_XML_ENDPOINT | Url of the mensa food XML-file | https://dummy.de/ |
| MENSA_NAME | Name of the mensa in the XML-file | "Mensa Campus Derendorf" |

Run the Script with `npm run bot`. Can be automated with a cronjob which runs this command every day.

## Create Cronjob
Runs the bot from Monday to Friday at 10 AM
```linux
(crontab -l ; echo "0 10 * * 1-5 node /${PATH_TO_MASTODON_REPO}/bots/mensa-bot/index.js") | crontab -
```