class CreatePassagesCommentRelations < ActiveRecord::Migration[6.1]
  def change
    create_table :passages_comment_relations do |t|
      t.bigint :passage_id, null: false, index: true
      t.bigint :comment_id, null: false, index: true

      t.timestamps
    end
    
  add_foreign_key :passages_comment_relations, :passages
  add_foreign_key :passages_comment_relations, :comments
  end
end
