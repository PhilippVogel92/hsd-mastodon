# frozen_string_literal: true

class HomeFeed < Feed
  def initialize(account)
    @account = account
    super(:home, account.id)
  end

  def regenerating?
    redis.exists?("account:#{@account.id}:regeneration")
  end

  def get(limit, max_id = nil, since_id = nil, min_id = nil, recommendations = false)
    limit    = limit.to_i
    max_id   = max_id.to_i if max_id.present?
    since_id = since_id.to_i if since_id.present?
    min_id   = min_id.to_i if min_id.present?

    if recommendations
      status_ids = from_redis(limit, max_id, since_id, min_id).ids
      recommended_toots = get_recommendations(status_ids, limit, max_id, since_id, min_id)
      ids = recommended_toots.collect {|id| Status.find(id) }
    else
      status_ids = from_redis(limit, max_id, since_id, min_id)
    end

  end

  def get_recommendations(status_ids, limit, max_id = nil, since_id = nil, min_id = nil)
    headers = { 'Content-Type': 'application/json' }
    response = Net::HTTP.post(URI(ENV["RECOMMENDER_URL"] + "accounts/#{@account.id}/create-sorted-timeline"), { "status_ids": status_ids, "ranking_score_treshold": 0.1 }.to_json, headers)
    JSON.parse(response.body)
  end

end
