import pandas as pd
from mastodon import Mastodon
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import html2text
import time

load_dotenv()

path = "./data"
isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)

instance = "mastodon.social"

mastodon = Mastodon(
    api_base_url=f"https://{instance}",
)

all_toots = mastodon.timeline_public(limit=40)

while len(all_toots) < 100000:
    smallest = all_toots[-1].id
    # toots_df = pd.DataFrame(mastodon.timeline_public(max_id=smallest, limit=40))
    all_toots.extend(mastodon.timeline_public(max_id=smallest, limit=40))
    # all_toots = pd.concat([all_toots, toots_df], ignore_index=True)
    df = pd.DataFrame(all_toots)
    df["content"] = df["content"].apply(lambda x: html2text.html2text(x))
    df["instance"] = instance
    df.to_csv(f"data/{instance}_toots.csv", index=False, sep=";")
