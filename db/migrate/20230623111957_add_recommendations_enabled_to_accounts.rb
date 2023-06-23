class AddRecommendationsEnabledToAccounts < ActiveRecord::Migration[6.1]
  def change
    add_column :accounts, :recommendations_enabled, :boolean, default: true
  end
end
