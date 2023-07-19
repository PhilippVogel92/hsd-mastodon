# frozen_string_literal: true

class InterestRelationshipsPresenter
  attr_reader :following_map

  def initialize(interests, current_account_id = nil, **options)
    @following_map = begin
      if current_account_id.nil?
        {}
      else
        InterestFollow.select(:interest_id).where(interest_id: interests.map(&:id), account_id: current_account_id).each_with_object({}) { |f, h| h[f.interest_id] = true }.merge(options[:following_map] || {})
      end
    end
  end
end
