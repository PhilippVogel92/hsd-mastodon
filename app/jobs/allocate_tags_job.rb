class AllocateTagsJob < ApplicationJob
  queue_as :default

  def perform(status_id)
    Net::HTTP.get(URI(ENV['RECOMMENDER_URL'] + "/statuses/#{status_id}/generate-tags"))
  end

  def max_attempts
    1
  end
end
