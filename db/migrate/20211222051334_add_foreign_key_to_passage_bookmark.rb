class AddForeignKeyToPassageBookmark < ActiveRecord::Migration[6.1]
  def change; end

  add_foreign_key :passage_bookmarks, :users
end
