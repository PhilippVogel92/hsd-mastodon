class CreateInterestFollows < ActiveRecord::Migration[6.1]
  def change
    create_table :interest_follows do |t|
      t.belongs_to :interest, null: false, foreign_key: { on_delete: :cascade }
      t.belongs_to :account, null: false, foreign_key: { on_delete: :cascade }, index: false

      t.timestamps

      t.index [:account_id, :interest_id], unique: true
    end
  end
end
