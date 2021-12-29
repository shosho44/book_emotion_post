class CreateComments < ActiveRecord::Migration[6.1]
  def change
    create_table :comments do |t|
      t.string :user_id, null: false, foreign_key: true, index: true
      t.text :content, null: false

      t.timestamps
    end

    add_index :comments, :id, unique: true

    add_foreign_key :comments, :users
  end
end
