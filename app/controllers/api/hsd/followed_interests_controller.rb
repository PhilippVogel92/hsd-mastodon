# frozen_string_literal: true

class Api::Hsd::FollowedInterestsController < Api::BaseController
  INTERESTS_LIMIT = 100

  before_action -> { doorkeeper_authorize! :follow, :read, :'read:follows' }
  before_action :require_user!
  before_action :set_results

  def index
    render json: @results.map(&:interest), each_serializer: REST::InterestSerializer, relationships: InterestRelationshipsPresenter.new(@results.map(&:interest), current_user&.account_id)
  end

  private

  def set_results
    @results = InterestFollow.where(account: current_account).joins(:interest).eager_load(:interest).to_a_paginated_by_id(
      limit_param(INTERESTS_LIMIT),
      params_slice(:max_id, :since_id, :min_id)
    )
  end
end
