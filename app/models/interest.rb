# frozen_string_literal: true

# == Schema Information
#
# Table name: interests
#
#  id             :bigint(8)        not null, primary key
#  name           :string
#  display_name   :string
#  last_status_at :datetime
#  created_at     :datetime         not null
#  updated_at     :datetime         not null
#

class Interest < ApplicationRecord
  has_and_belongs_to_many :statuses
  has_and_belongs_to_many :accounts

end
