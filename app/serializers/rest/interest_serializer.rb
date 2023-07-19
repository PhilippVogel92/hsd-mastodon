# frozen_string_literal: true

class REST::InterestSerializer < ActiveModel::Serializer
  include RoutingHelper

  attributes :name

  attribute :following, if: :current_user?

  def name
    object.display_name
  end

  def following
    if instance_options && instance_options[:relationships]
      instance_options[:relationships].following_map[object.id] || false
    else
      InterestFollow.where(interest_id: object.id, account_id: current_user.account_id).exists?
    end
  end

  def current_user?
    !current_user.nil?
  end
end
