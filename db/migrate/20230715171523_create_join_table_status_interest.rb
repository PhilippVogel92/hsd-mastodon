class CreateJoinTableStatusInterest < ActiveRecord::Migration[6.1]
  def change
    create_join_table :statuses, :interests do |t|
      t.index :interest_id
      t.index [:interest_id, :status_id], unique: true
    end
  end
end
