class CreateInterests < ActiveRecord::Migration[6.1]
  def change
    create_table :interests do |t|
      t.string :name
      t.string :display_name
      t.datetime :last_status_at

      t.timestamps
    end
  end
end
