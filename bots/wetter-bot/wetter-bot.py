from mastodon import Mastodon
import datetime
import json   
import urllib.request

api_url = "https://wttr.in/duesseldorf_mplang=de.png"




#download image
def get_Image(api_url, filename):
    urllib.request.urlretrieve(api_url, filename);





if __name__ == "__main__":
	# Setup mastodon connection:
	mastodon = Mastodon(
    	access_token = 'sJYGYFq7-cDBW9p06QM_9UuPTAnpAQQlG_zLnZWCyiA',
   		api_base_url = 'http://mastodon.hosting.medien.hs-duesseldorf/'
	)

	get_Image(api_url, "weather.png")

	media_dict = mastodon.media_post("weather.png")
	print(media_dict["id"])


	status_dict = mastodon.status_post("Wetterbericht. (API: https://github.com/chubin/wttr.in) ", media_ids=media_dict);
	print(status_dict)
