class AllocateTagsJob < ApplicationJob
  queue_as :default

  def perform(toot_id)
    http = Net::HTTP.new("localhost", 5000)
    http.use_ssl = false
    request = Net::HTTP::Post.new("toots/#{toot_id}/generate-tags")
    http.request(request)
  end
end
