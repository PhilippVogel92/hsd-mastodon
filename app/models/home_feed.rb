# frozen_string_literal: true

class HomeFeed < Feed
  def initialize(account)
    @account = account
    super(:home, account.id)
  end

  def regenerating?
    redis.exists?("account:#{@account.id}:regeneration")
  end

  def get(limit, max_id = nil, since_id = nil, min_id = nil, recommendations = false, status_count = nil)
    limit    = limit.to_i
    max_id   = max_id.to_i if max_id.present?
    since_id = since_id.to_i if since_id.present?
    min_id   = min_id.to_i if min_id.present?
    status_count   = status_count.to_i if status_count.present?

    if recommendations
      from_redis_recommender(limit, max_id, since_id, status_count)
    else
      from_redis(limit, max_id, since_id, min_id)
    end
  end

  def from_redis_recommender(limit, max_id, since_id, status_count)
    interests_for_account = InterestFollow.by_account(@account.id).pluck(:interest_id)
    statuses_by_account_interests = Status.by_interests(interests_for_account).ids
    # todo get tags by interest names
    interest_tags_for_account = Tag.by_account_interests(interests_for_account).ids
    statuses_by_interest_tags = Status.tagged_with(interest_tags_for_account).ids
    recommender_pooling_statuses = statuses_by_account_interests.union(statuses_by_interest_tags)

    recommender_feed_key = key_recommender
    if redis.exists(recommender_feed_key).zero?
      home_feed_ids = redis.zrevrangebyscore(key, '(+inf', '(-inf').map(&:to_i)
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug(home_feed_ids.count)
      Rails.logger.debug(recommender_pooling_statuses.count)
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      home_feed_ids = home_feed_ids.union(recommender_pooling_statuses)

      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug(home_feed_ids.count)
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      Rails.logger.debug("")
      recommended_toots = get_recommendations(home_feed_ids)
      return [] if recommended_toots.empty?
      redis.rpush(recommender_feed_key, recommended_toots)
      status_ids = recommended_toots.take(limit)
    else
      if since_id.blank?
        start_pos = status_count
        end_pos = start_pos + limit - 1
      else
        start_pos = 0
        recommender_feed_len = redis.llen(recommender_feed_key)
        return [] if (recommender_feed_len - status_count).zero?
        end_pos = recommender_feed_len - status_count - 1
        end_pos = limit - 1 if end_pos > limit - 1
      end
      status_ids = redis.lrange(recommender_feed_key, start_pos, end_pos).map(&:to_i)
      status_ids = status_ids.take(status_ids.index(since_id) || limit) if since_id.present?
    end
    Status.where(id: status_ids).sort_by { |status| status_ids.index(status.id) }
  end

  def key_recommender(subtype = nil)
    return FeedManager.instance.key(@type, @id, 'recommender') unless subtype

    FeedManager.instance.key(@type, @id, "recommender:#{subtype}")
  end

  def get_recommendations(status_ids)
    headers = { 'Content-Type': 'application/json' }
    begin
      response = Net::HTTP.post(URI(ENV['RECOMMENDER_URL'] + "accounts/#{@account.id}/create-sorted-timeline"), { "status_ids": status_ids}.to_json, headers)
    rescue StandardError
      raise Mastodon::RecommenderConnectionRefusedError, I18n.t('recommender.error.connection_refused')
    else
      if response.code == '200'
        JSON.parse(response.body)
      else
        raise Mastodon::RecommenderResponseError, I18n.t('recommender.error.recommender_response')
      end
    end
  end

end
