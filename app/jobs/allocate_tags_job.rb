class AllocateTagsJob < ApplicationJob
  queue_as :default

  def perform(status_id)
    headers = {'Content-Type': 'application/json'}
    Net::HTTP.post(URI(ENV['RECOMMENDER_URL'] + "/statuses/#{status_id}/generate-tags"), nil, headers)
  end

  def max_attempts
    1
  end
end
