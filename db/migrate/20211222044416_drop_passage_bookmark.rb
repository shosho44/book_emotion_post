class DropPassageBookmark < ActiveRecord::Migration[6.1]
  def change
    remove_foreign_key :passage_bookmarks, :passages
    drop_table 'passage_bookmarks', force: :cascade do |t|
      t.string 'user', null: false
      t.integer 'passage_id', null: false
      t.datetime 'created_at', precision: 6, null: false
      t.datetime 'updated_at', precision: 6, null: false
      t.index ['passage_id'], name: 'index_passage_bookmarks_on_passage_id'
      t.index ['user'], name: 'index_passage_bookmarks_on_user'
    end
  end
end
