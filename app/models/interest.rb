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
  
  INTEREST_SEPARATORS = "_\u00B7\u30FB\u200c"
  INTEREST_FIRST_SEQUENCE_CHUNK_ONE = "[[:word:]_][[:word:]#{INTEREST_SEPARATORS}]*[[:alpha:]#{INTEREST_SEPARATORS}]"
  INTEREST_FIRST_SEQUENCE_CHUNK_TWO = "[[:word:]#{INTEREST_SEPARATORS}]*[[:word:]_]"
  INTEREST_FIRST_SEQUENCE = "(#{INTEREST_FIRST_SEQUENCE_CHUNK_ONE}#{INTEREST_FIRST_SEQUENCE_CHUNK_TWO})"
  INTEREST_LAST_SEQUENCE = '([[:word:]_]*[[:alpha:]][[:word:]_]*)'
  INTEREST_NAME_PAT = "#{INTEREST_FIRST_SEQUENCE}|#{INTEREST_LAST_SEQUENCE}"
  INTEREST_NAME_RE = /\A(#{INTEREST_NAME_PAT})\z/i

  class << self
    def find_normalized(name)
      matching_name(name).first
    end

    def find_normalized!(name)
      find_normalized(name) || raise(ActiveRecord::RecordNotFound)
    end

    def normalize(str)
      HashtagNormalizer.new.normalize(str)
    end

    def matching_name(name_or_names)
      names = Array(name_or_names).map { |name| arel_table.lower(normalize(name)) }

      if names.size == 1
        where(arel_table[:name].lower.eq(names.first))
      else
        where(arel_table[:name].lower.in(names))
      end
    end
  end
end
