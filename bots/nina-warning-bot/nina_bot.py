import html
import os

import requests
import logging

from dotenv import load_dotenv
from mastodon import Mastodon

from requests import JSONDecodeError

load_dotenv()

# The base url for the German official warning system API
NINA_API_URL = "https://warnung.bund.de/api31"

# Region code can be obtained from
# https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07-31/download/Regionalschl_ssel_2021-07-31.json
# Please note that you have to substitute all digits starting from the 6th digit with 0.
REGION_CODE = str(os.environ.get("REGION_CODE"))

# Blacklist file location, used to store the IDs of the warnings this bot has already posted
BLACKLIST_FILE = os.environ.get("BLACKLIST_FILE")

# Mastodon API Credentials
MASTODON_API_BASE_URL = os.environ.get("MASTODON_API_BASE_URL")
MASTODON_API_ACCESS_TOKEN = os.environ.get("MASTODON_API_ACCESS_TOKEN")


# Makes a request and returns the JSON response as a dictionary
def make_request(relative_url: str):
    response = requests.get(NINA_API_URL + relative_url)
    response_json = {}

    # If the request status code is not in the 200 range, we will log the error and exit the script
    if response.status_code < 200 or response.status_code > 229:
        logging.critical("Error in NINA bot: API returned status code {} at endpoint {}".format(
          str(response.status_code), relative_url))
        exit(1)

    # The response format should be JSON. If not, a warning will be logged and the program will be terminated.
    try:
        response_json = response.json()
    except JSONDecodeError:
        logging.critical("Error in NINA bot: Could not decode JSON response! Response was " + str(response.content))
        exit(1)

    return response_json


# Initialize Mastodon
mastodon = Mastodon(
  access_token=MASTODON_API_ACCESS_TOKEN,
  api_base_url=MASTODON_API_BASE_URL
)


# Get all warnings for a specific region
all_warnings = make_request("/dashboard/" + REGION_CODE + ".json")

# Get all warning IDs that were posted already
try:
    with open(BLACKLIST_FILE, "r") as f:
        warnings_already_posted = f.read().splitlines()
except FileNotFoundError:
    warnings_already_posted = []

# Used to store the warning IDs that will be posted by this script now
warnings_posted_now = []


for warning in all_warnings:
    # The dashboard only contains basic information about the warning. That is why we need to retrieve more details.
    warning_id = warning["payload"]["id"]

    # If this bot has already posted the warning, it will be ignored.
    if warning_id in warnings_already_posted:
        continue

    # Get the details of a warning
    warning_details = make_request("/warnings/" + warning_id + ".json")

    # Combine both the headline and the description into a string to post on Mastodon
    headline = warning_details["info"][0]["headline"]
    event = warning_details["info"][0].get("event", "WARNUNG").upper()
    # If the value in the "event" field does not make sense, we want to substitute it with a generic warning
    if len(event) < 4 or event.isnumeric():
        event = "WARNUNG"
    description = html.unescape(warning_details["info"][0]["description"]).replace("<br/>", "\n")
    if warning_details["msgType"] == "Cancel":
        warning_text = "✅ Entwarnung ✅\n{}\n\n{}".format(headline, description)
    else:
        warning_text = "⚠️ {} ⚠️\n{}\n\n{}".format(event, headline, description)

    # Mastodon allows up to 500 characters. If our text exceeds this limit, it will be cut.
    if len(warning_text) > 500:
        warning_text = warning_text[0:449] + "...\n\nMehr Infos über die offiziellen Warnkanäle."

    # Post the warning to Mastodon
    mastodon.status_post(warning_text, visibility="public", language="de")

    # Log some information about the warning
    logging.info("NINA bot posted warning with ID {} and headline {}".format(warning_id, headline))

    # Add the warning to the list pending to be added to the blacklist file
    warnings_posted_now.append(warning_id)

# Add the warnings that were just posted to the blacklist file
if warnings_posted_now:
    with open(BLACKLIST_FILE, "a+") as f:
        f.write('\n'.join(warnings_posted_now))
        f.write('\n')
