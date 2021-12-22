class CreatePassageBookmark < ActiveRecord::Migration[6.1]
  def change
    create_table :passage_bookmarks do |t|
      t.string :user_id, foreign_key: { to_table: :users }, null: false, index: true
      t.references :passage, foreign_key: { to_table: :passages }, null: false, index: true

      t.timestamps
    end
  end
end
