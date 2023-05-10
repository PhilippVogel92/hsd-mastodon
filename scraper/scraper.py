import pandas as pd 
from mastodon import Mastodon
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os 
import html2text 
import time
load_dotenv()

instances= [
    "mastodon.social",
    #"troet.cafe",
    #"sueden.social",
    #"norden.social",
    #"nrw.social",
    #"social.cologne",
    #"muenchen.social",
]

path = "./data"
isExist = os.path.exists(path)
if not isExist:
   os.makedirs(path)

for instance in instances:
    mastodon = Mastodon(api_base_url = f'https://{instance}', 
                    client_id = os.environ.get('SECRET'),
                    client_secret=os.environ.get('SECRET'))
    toots = mastodon.timeline_public(min_id=None, limit=40)
    while len(toots) < 100000:
        mastodon = Mastodon(api_base_url = f'https://{instance}', 
                    client_id = os.environ.get('SECRET'),
                    client_secret=os.environ.get('SECRET'))
        smallest = toots[-1].id if len(toots) > 0 else None
        toots.extend(mastodon.timeline_public(min_id=smallest, limit=40))
        toots_df = pd.DataFrame(toots)
        toots_df['content'] = toots_df['content'].apply(lambda x: html2text.html2text(x))
        toots_df = toots_df[['id', 
                        'content',
                        'reblogs_count', 
                        'favourites_count', 
                        'replies_count',
                        'mentions', 
                        'tags', 
                        'language', 
                        'created_at', 
                        'edited_at']]
        toots_df = toots_df.rename(columns={"id": "toot_id"})
        toots_df['instance'] = instance
        toots_df.to_csv(f'data/{instance}_toots.csv',index=False, sep=';')

all_instances_toots = pd.DataFrame()
for instance in instances:
    df = pd.read_csv(f'{path}/{instance}_toots.csv', sep=';')
    all_instances_toots = pd.concat([all_instances_toots, df], ignore_index=True)

shuffled_toots = all_instances_toots.sample(frac = 1)
shuffled_toots.to_csv(f'{path}/all_toots.csv',index=False, sep=';')
exit()