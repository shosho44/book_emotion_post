class CreatePassageBookmarks < ActiveRecord::Migration[6.1]
  def change
    create_table :passage_bookmarks do |t|
      t.string :user_id, null: false, foreign_key: true, index: true
      t.bigint :passage_id, null: false, foreign_key: true, index: true

      t.timestamps
    end

    add_foreign_key :passage_bookmarks, :users
    add_foreign_key :passage_bookmarks, :passages
  end
end
