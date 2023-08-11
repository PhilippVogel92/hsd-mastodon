import os

from dotenv import load_dotenv
import requests
import logging

load_dotenv()

# The base url for the German official warning system API
NINA_API_URL: str = "https://warnung.bund.de/api31"

# Region code can be obtained from
# https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07-31/download/Regionalschl_ssel_2021-07-31.json
# Please note that you have to substitute all digits starting from the 6th digit with 0.
REGION_CODE: str = str(os.environ.get("REGION_CODE"))

# Blacklist file location, used to store the IDs of the warnings this bot has already posted
BLACKLIST_FILE: str = os.environ.get("BLACKLIST_FILE")

# We need to obtain all warnings that are currently active. This is to prevent deleting any currently active
# warning IDs from the blacklist file. Doing so would result in duplicate posts.
active_warnings = {}
try:
    active_warnings = requests.get(f'{NINA_API_URL}/dashboard/{REGION_CODE}.json').json()
except requests.JSONDecodeError:
    logging.critical("Error in NINA bot cleanup script: Could not decode JSON response!")

# Get all warning IDs that were posted already
warnings_in_blacklist_file: list = []
try:
    with open(BLACKLIST_FILE, "r") as f:
        warnings_in_blacklist_file = f.read().splitlines()
except FileNotFoundError:
    warnings_in_blacklist_file = []

# This is the list of warnings that should be included in the cleaned up blacklist file. These are warnings that are
# still active but have already been posted to Mastodon.
warnings_cleaned_up: list = []

for warning in active_warnings:
    warning_id: str = warning["payload"]["id"]
    if warning_id in warnings_in_blacklist_file:
        warnings_cleaned_up.append(warning_id)

# Clear file and add any cleaned up warnings
with open(BLACKLIST_FILE, "w") as f:
    f.write('\n'.join(warnings_cleaned_up))
    f.write('\n')

