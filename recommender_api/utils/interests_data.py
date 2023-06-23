import pandas as pd
from pytrends.request import TrendReq
from functools import reduce 
from ..model.mastodon_data_db import persist_tag, get_tag_by_name

def get_google_trends():
    pytrend = TrendReq()
    trends = pytrend.realtime_trending_searches(pn='DE')
    trend_titles = trends["title"].apply(lambda x: x.split(','))
    trend_titles = reduce(lambda a, b: a+b, trend_titles)
    trend_titles = [title.replace(',', '').strip().replace(' ', '_').replace('(', '').replace(')', '').replace('.', '_').replace("'", '_').replace(':', '_').replace('/', '_').replace('-', '_').replace('__', '_') for title in trend_titles]
    trend_titles = set(trend_titles)
    trend_titles = (list(trend_titles))
    [persist_tag(title) for title in trend_titles if get_tag_by_name(title.lower()) is None]
