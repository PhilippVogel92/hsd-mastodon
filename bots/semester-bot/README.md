# Mastodon semester progress bot

This bot generates and posts progress bars for completed lecture and exam phases of a semester. It attaches a dynamically created PNG image of a progress bar to each post.

## Configuration
The configuration parameters are loaded from the environment variables or from a .env file in the directory of the bot
script (`bot.js`).

The following parameters must be set:
| Name | Description | Example |
| ---- | ----------- | ------- |
| `BOT_API_URL` | The URL to the Mastodon instance. | https://mastodon.hosting.medien.hs-duesseldorf.de/ |
| `ACCESS_TOKEN` | The access token to authenticate with the Mastodon API. | ... |
| `SEMESTER_XML_ENDPOINT` | The endpoint for the semester information. | https://medien.hs-duesseldorf.de/studium/_api/Web/Lists(guid'c8932ccb-dbee-478f-a615-0e2e3f17304d')/Items |

## Usage
This bot is written in Node.js. It requires some dependencies which can be installed by running `node install` from the bot's directory. 

You can run the script with the following command: `node bot.js`

This script is intended to run on Mondays and Fridays through a cronjob.
