# frozen_string_literal: true

class Api::Hsd::InterestsController < Api::BaseController
  before_action -> { doorkeeper_authorize! :follow, :write, :'write:follows' }, except: [:show, :search]
  before_action :require_user!, except: :show
  before_action :set_or_create_interest, except: :search
  before_action :set_search_results, only: :search

  def show
    render json: @interest, serializer: REST::InterestSerializer
  end

  def search
    render json: @search_results, each_serializer: REST::InterestSerializer
  end

  def follow
    InterestFollow.create_with(rate_limit: true).find_or_create_by!(interest: @interest, account: current_account)
    del_key_recommender(current_account.id)
    render json: @interest, serializer: REST::InterestSerializer
  end

  def unfollow
    InterestFollow.find_by(account: current_account, interest: @interest)&.destroy!
    del_key_recommender(current_account.id)
    render json: @interest, serializer: REST::InterestSerializer
  end

  private

  def set_or_create_interest
    return not_found unless Interest::INTEREST_NAME_RE.match?(params[:id])
    @interest = Interest.find_normalized(params[:id]) || Interest.new(name: Interest.normalize(params[:id]), display_name: params[:id])
  end

  private

  def set_search_results
    @search_results = Interest.where("name LIKE :search", search: "#{params[:q]}%")
  end
end
