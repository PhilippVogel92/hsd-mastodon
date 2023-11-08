# HSD Mastodon Recommender System

## Overview
The HSD Mastodon Recommender System is an advanced feature implemented within the HSD Mastodon instance that aims to curate and personalize the Mastodon timeline for each user. By leveraging a sophisticated ranking algorithm, the system prioritizes posts that are more likely to be of interest to the user, thereby creating an engaging and relevant social media experience.

## Key Features
- **Ranking System**: A comprehensive framework that calculates a score for each post to determine its relevance to the user's interests.
- **Status Filtering**: Utilizes a score threshold to filter out less relevant posts and employs techniques to ensure a diverse range of authors is presented to the user.
- **Status Sorting**: Organizes posts in descending order of relevance based on their calculated ranking scores to present the most pertinent content first.
- **Interest Modeling**: Enables the adaptation of a user's timeline to their interests by associating relevant interests with each post.
  
## Detailed Description of Recommender System
The Recommender System is the heartbeat of the HSD Mastodon instance's personalized timeline. It compiles a list of posts ranked according to user engagement, relevance to user's interests, relationships between the user and post authors, and the freshness of posts.

![Komponentensicht_lv1 drawio](https://github.com/PhilippVogel92/hsd-mastodon/assets/107690428/3a8014ea-925a-45ae-a32a-9be704bf6e8b)

The ranking system is built upon several key components:

### Ranking Calculator
Handles the complex task of evaluating the relevance of posts within the home timeline. The system considers several elements:

- **Interaction Subscores**: Derived from different forms of post engagement, such as comments (replies), shares (reblogs), and likes (favourites). The subscore formula ensures that scores range between 0 and 1, increasing progressively with the number of engagements. Tunable parameters allow for adjusting sensitivity to engagement frequency, accommodating for the instance's activity level.
- **Weighted Interaction Score**: A combined, weighted sum of all interaction subscores, where each type of interaction is assigned a distinct importance and the total does not exceed 1.
- **Age Score**: Reflects the timeliness of a post, depreciating over time but never plummeting to zero. This score is also configurable to modulate its impact on the overall ranking.
- **Follower & Interest Boost**: Additional scores are applied to promote content from followed users and topics aligned with the user's interests.

### Status Filtering
Focused on enhancing the diversity of content shown to users, the status filter operates to:

- **Promote Author Diversity**: Limit the predominance of prolific authors by setting daily per-author post visibility limits, ensuring a breadth of perspectives within the user's feed.
- **Threshold-Based Filtering**: Exclude posts scoring below a certain threshold, typically filtering out content from muted or blocked authors to accommodate user preferences and foster a positive environment.
  
![Komponentensicht_lv2_ranking drawio (1)](https://github.com/PhilippVogel92/hsd-mastodon/assets/107690428/df2b398c-5a6b-4a81-a149-3c1bdd3edc63)

### Interest Modeling

The Interest Modeling in the Recommender System plays a pivotal role in personalizing the user experience by associating relevant interests with statuses posted within the Mastodon network.

#### Data Foundation for Interest Assignment

The `InterestGenerator` class requires only the status ID and utilizes this information to fetch necessary data from the Mastodon database. This data foundation ensures that the size of the request body originating from the Mastodon instance is kept minimal.

#### Dynamic Model Selection for Each Status

For keyword extraction and interest assignment, various Natural Language Processing (NLP) models, supported by SpaCy, are employed based on the language of the status. The class `InterestGenerator` includes the `choose_nlp_model` method selecting suitable NLP models for analyzing text based on its detected language, using the `langdetect` library. This dynamic selection ensures high precision in keyword extraction.

#### Keyword Extraction and Text Preprocessing
The TextPreprocessor class is responsible for preparing the status text by removing HTML tags, URLs, and stop words, while also converting words to their base or lemma form. This preprocessing streamlines the text and improves the accuracy of keyword extraction by removing unnecessary information.

#### Interest Analysis and Assignment based on Keywords
The InterestGenerator class performs interest analysis and assignment by comparing the extracted and preprocessed keywords with existing interests in the Mastodon database. Both keywords and interests are transformed into word vectors using the selected NLP model. Similarity between the vectors is then calculated using cosine similarity. Matches above a predefined threshold are considered relevant and are used to recommend interests to the status. The three highest-scoring interests are assigned to the status, enhancing personalization.

![Komponentensicht_lv2_interest drawio (1)](https://github.com/PhilippVogel92/hsd-mastodon/assets/107690428/91af78bb-2c4f-488e-93fa-9bd09d7e173a)

### Recommender API Endpoints

The Recommender's routing is realized through the Flask micro-framework, enabling the processing of Mastodon instance requests and invocation of the corresponding controller functions. Our Flask-Blueprint class outlines the endpoints responsible for generating a sorted timeline and determining interests for posts, as highlighted below:

| Method  | Path                                         | Description                                              |
|---------|----------------------------------------------|----------------------------------------------------------|
| POST    | /accounts/<account_id>/create-sorted-timeline | Returns a sorted list of status IDs based on the recommendation algorithm.|
| GET     | /statuses/<status_id>/generate-interests      | Returns interests associated with a status.              |


### Integration with Mastodon's Ruby on Rails and React Applications

The recommender system seamlessly integrates with both the Ruby on Rails and React parts of the Mastodon project. All modifications are currently exclusive to the HSD instance but have been developed with the potential future inclusion into the open-source project in mind.

## Getting Started

To set up and run the recommender system on your Mastodon instance, ensure you have the following prerequisites:
- Ruby version
- Rails version
- Mastodon version
- Flask micro-framework for Python

Follow the instructions to integrate the recommender system and foster a more engaging and personalized social experience for your users.

### Installation

1. Clone the repository to your local machine.
2. Install the required dependencies for Ruby on Rails and Flask.
3. Run database migrations if necessary.
4. Start the Rails server.
5. Set up the Flask application to handle recommendation API endpoints.

### Usage

After successful integration, use the Mastodon UI to interact with the recommender system. Users can benefit from options that allow toggling between the original chronological feed and the new recommender feed, thus controlling the display of recommended posts.


## License

This recommender system is distributed under the [LICENSE.md](LICENSE.md) included with the project. It stipulates the terms under which the software may be used, modified, and distributed.

## Authors
- Philipp Vogel (Recommender Architecture, Interest Modeling, Status Filtering/Sorting, API Endpoints)
- Kevin Zielke (Ranking Calculator)
- Nils Remigius (Recommender API Binding, Redis/Mastodon Integration)
- Ben Kräling (Recommender API Binding, Interest Modeling, Frontend Mastodon Recommender Feed)
- Simon Ludwig, Valeriia Muzhevska, Eric Oelsen (Bots)
- Dario Varivoda (Server Backup, Hosting, CI/CD)
 
## Acknowledgments

The authors extend their gratitude to the HSD community, Mastodon open-source contributors, and all who have provided feedback and support throughout the development of this recommender system.
