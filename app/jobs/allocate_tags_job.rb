class AllocateTagsJob < ApplicationJob
  queue_as :default

  def perform(status_id)
    http = Net::HTTP.new("localhost", 5000)
    http.use_ssl = false
    request = Net::HTTP::Post.new("statuses/#{status_id}/generate-tags")
    http.request(request)
  end

  def max_attempts
    1
  end
end
