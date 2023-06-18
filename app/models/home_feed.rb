# frozen_string_literal: true

require 'json'

class HomeFeed < Feed
  def initialize(account)
    @account = account
    super(:home, account.id)
  end

  def regenerating?
    redis.exists?("account:#{@account.id}:regeneration")
  end

  def get(limit, max_id = nil, since_id = nil, min_id = nil)
    limit    = limit.to_i
    max_id   = max_id.to_i if max_id.present?
    since_id = since_id.to_i if since_id.present?
    min_id   = min_id.to_i if min_id.present?


    # a) send cache ids to python api
    # b) fetch toots by cache ids and send to python api

    http = Net::HTTP.new("localhost", 8081)
    http.use_ssl = false

    request = Net::HTTP::Post.new("recommend-tfidf", 'Content-Type' => 'application/json')
    request.body = {"sentence": "Hey Ben!", "number_of_recommendations": 10}.to_json

    response = http.request(request)

    logger = Logger.new("log/my_logneu.log")
    cache_ids = from_redis(limit, max_id, since_id, min_id)
    logger.debug cache_ids
    cache_ids

    # retrieve sorted toots from python api

    # get toots of authenticated user
  
    

  end
end
