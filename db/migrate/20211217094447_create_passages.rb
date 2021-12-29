class CreatePassages < ActiveRecord::Migration[6.1]
  def change
    create_table :passages do |t|
      t.string :user_id, null: false, foreign_key: true
      t.string :book_title, default: '', null: false
      t.text :content, null: false

      t.timestamps
    end

    add_index :passages, :id, unique: true
    add_index :passages, :user_id

    add_foreign_key :passages, :users
  end
end
