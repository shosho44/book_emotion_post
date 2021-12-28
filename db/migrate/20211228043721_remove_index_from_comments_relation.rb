class RemoveIndexFromCommentsRelation < ActiveRecord::Migration[6.1]
  def change
    remove_index :comments_relations, :child_comment_id
  end
end
