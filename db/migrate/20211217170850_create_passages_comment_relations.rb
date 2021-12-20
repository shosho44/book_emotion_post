class CreatePassagesCommentRelations < ActiveRecord::Migration[6.1]
  def change
    create_table :passages_comment_relations do |t|
      t.integer :passage_id
      t.integer :comment_id

      t.timestamps
    end
  end
end
