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

    if(recommendations)
      status = from_redis(limit, max_id, since_id, min_id)
    else
      status = from_redis(limit, max_id, since_id, min_id)
      status.sort()
    end

    # reorder
  end


end
