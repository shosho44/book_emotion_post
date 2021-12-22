class AddForeignKeyToCommentLike < ActiveRecord::Migration[6.1]
  def change; end
  add_foreign_key :comment_likes, :users
end
