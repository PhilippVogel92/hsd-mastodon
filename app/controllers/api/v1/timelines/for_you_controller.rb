# frozen_string_literal: true

class Api::V1::Timelines::ForYouController < Api::BaseController
  before_action :require_user!, only: [:show], if: :require_auth?
  after_action :insert_pagination_headers, unless: -> { @statuses.empty? }
  def show
    @statuses = load_statuses
    @statuses.sort!
    render json: @statuses, each_serializer: REST::StatusSerializer,
           relationships: StatusRelationshipsPresenter.new(@statuses, current_user&.account_id)
  end

  private

  def require_auth?
    !Setting.timeline_preview
  end

  def load_statuses
    cached_for_you_statuses
  end

  def cached_for_you_statuses
    cache_collection for_you_statuses, Status
  end

  def for_you_statuses
    # statuses = public_feed.get(1000)
    statuses = Status.all
    request = Request.new(:post, ENV.fetch('RECOMMENDER_DOMAIN', nil),
                          body: {
                            'dataset' => statuses,
                            'number_of_recommendations' => statuses.size,
                            'user' => current_user.account,
                          }.to_json)
    request.add_headers({ 'Content-Type': 'application/json' })
    request.perform do |response|
      recommendations = JSON.parse(response)
      Rails.logger.debug { "Recommendations: #{recommendations}" }
    end
    statuses
  end

  def public_feed
    PublicFeed.new(current_account)
  end

  def insert_pagination_headers
    set_pagination_headers(next_path, prev_path)
  end

  def pagination_params(core_params)
    params.slice(:local, :limit).permit(:local, :limit).merge(core_params)
  end

  def next_path
    api_v1_timelines_for_you_url pagination_params(max_id: pagination_max_id)
  end

  def prev_path
    api_v1_timelines_for_you_url pagination_params(min_id: pagination_since_id)
  end

  def pagination_max_id
    @statuses.last.id
  end

  def pagination_since_id
    @statuses.first.id
  end
end
