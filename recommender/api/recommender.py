from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
import json

class Recommender:
   
    def __init__(self, toots):
        self.toots = toots

    def get_recommended_toots_for_account(self, account_id):
        self.create_tfidf_cosine_similarity_score(account_id)        

    def create_tfidf_cosine_similarity_score(self, account_id):
        tfidf_matrix = self.create_tfidf_matrix()
        cosine_sim_linear = linear_kernel(tfidf_matrix, tfidf_matrix)   
        account_toots = self.get_toots_by_account(account_id)

    def create_tfidf_matrix(self, content):
        tfidf_vectorizer = TfidfVectorizer()
        content = self.toots['content_lemma'] 
        return tfidf_vectorizer.fit_transform(content)

    def calculate_cosine_similarity(self, index, cosine_sim):
        sim_scores = list(enumerate(cosine_sim[index]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        sim_indices = [i[0] for i in sim_scores]
        return sim_indices
    
    def extract_account_data(self):
        self.toots["account_id"] = ""
        self.toots["account_username"] = ""
        self.toots["account_acct"] = ""
        self.toots["account_display_name"] = ""
        self.toots["account_locked"] = False
        self.toots["account_bot"] = False

        count=0
        errors = []
        for index, row in  self.toots.iterrows():
            try:
                account_str = row.account
                account_str = account_str.replace("\'", "\"").replace('False', 'false').replace("True","true")
                trim_field_index = account_str.find("discoverable")
                account_str = account_str[:trim_field_index-3] + "}"
                account_json = json.loads(account_str)
                self.toots.loc[index, "account_id"] = account_json["id"]
                self.toots.loc[index, "account_username"] = account_json["username"]
                self.toots.loc[index, "account_acct"] = account_json["acct"]
                self.toots.loc[index, "account_display_name"] = account_json["display_name"]
                self.toots.loc[index, "account_locked"] = account_json["locked"]
                self.toots.loc[index, "account_bot"] = account_json["bot"]
            except:
                pass


    def get_toots_by_account(self, account_id):
        mask = self.toots.account_id == account_id
        return self.toots[mask]