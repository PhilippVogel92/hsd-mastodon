import json
import requests
import pandas as pd
import os


def load_test_data(filename, path):
    data = pd.read_csv(os.path.join(path, filename), sep=";")

    # select only english and german toots
    mask_language = (data["language"] == "en") | (data["language"] == "de")
    data = data[mask_language]

    return data


def get_account_id(data):
    json_string = data.account.split(", 'display_name'")[0] + "}"
    json_string = json_string.replace("'", '"')
    json_string = json_string.replace("False", "false")
    json_string = json_string.replace("True", "true")
    json_object = json.loads(json_string)
    data.drop("account")
    return json_object["id"]


def get_account_toots(account_id):
    instance = "mastodon.hosting.medien.hs-duesseldorf.de"
    path = f"api/v1/accounts/{account_id}/statuses/"
    response = requests.get(url=f"https://{instance}/{path}")

    df = pd.DataFrame(data=response.json())
    return df


def get_followed_accounts(account_id):
    instance = "mastodon.hosting.medien.hs-duesseldorf.de"
    path = f"api/v1/accounts/{account_id}/following"
    response = requests.get(url=f"https://{instance}/{path}")

    account_ids = pd.DataFrame(data=response.json()).id.to_list()
    return account_ids
