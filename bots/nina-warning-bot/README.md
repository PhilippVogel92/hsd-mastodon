# Mastodon warning bot using the NINA API

This bot posts alerts and warnings that have been issued through the official German warning app [NINA](https://www.bbk.bund.de/DE/Warnung-Vorsorge/Warn-App-NINA/warn-app-nina_node.html).

## Configuration
The configuration parameters are loaded from the environment variables or from a _.env_ file in the directory of the bot
script (`nina_bot.py`).

The following parameters must be set:
| Name | Description | Example |
| ---- | ----------- | ------- |
| `REGION_CODE` | The region code of the targeted area. Can be obtained from [here](https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07-31/download/Regionalschl_ssel_2021-07-31.json). Please note: The last seven digits have to be zero because the API only works on a district/city level. | Region code for Düsseldorf: 051110000000 |
| `BLACKLIST_FILE` | Path where the blacklist file is stored. This blacklist is used to log which warnings the bot has already posted (to avoid duplicates). The file contains all IDs of the warnings posted, separated by a new line. If the file does not exist, it will be created after the first warning has been posted. | Absolute or relative path, e.g. `warnings_already_posted.txt` |
| `MASTODON_API_BASE_URL` | The URL to the Mastodon instance. | https://mastodon.hosting.medien.hs-duesseldorf.de/ |
| `MASTODON_API_ACCESS_TOKEN` | The access token to authenticate with the Mastodon API. | o20-snX... |

## Usage
This bot is written in Python. It requires Python 3 and some dependencies which can be installed by running `pip install -r requirements.txt`. 

The bot script will fetch all warnings for the desired region and post the ones it has not posted already.
You can run the script with the following command: `python nina_bot.py`

This script is intended to run periodically, e.g. through a cronjob. 

