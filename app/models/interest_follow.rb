# == Schema Information
#
# Table name: interest_follows
#
#  id          :bigint(8)        not null, primary key
#  interest_id :bigint(8)        not null
#  account_id  :bigint(8)        not null
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#
class InterestFollow < ApplicationRecord
  include RateLimitable
  include Paginable

  belongs_to :interest
  belongs_to :account

  scope :by_account, ->(account_id) { where(account_id: account_id) }

end
