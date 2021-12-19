class ChangeColumnsToPassagesCommentRelation < ActiveRecord::Migration[6.1]
  def change
    remove_column :passages_comment_relations, :passage_id
    add_reference :passages_comment_relations, :passage, null: false, foreign_key: true, index: true
    remove_column :passages_comment_relations, :comment_id
    add_reference :passages_comment_relations, :comment, null: false, foreign_key: true
  end

  add_foreign_key :passages_comment_relations, :passages, column: :passage_id, primary_key: :id
  add_foreign_key :passages_comment_relations, :comments, column: :comment_id, primary_key: :id
end
