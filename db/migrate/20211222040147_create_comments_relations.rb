class CreateCommentsRelations < ActiveRecord::Migration[6.1]
  def change
    create_table :comments_relations do |t|
      t.bigint :parent_comment_id, foreign_key: { to_table: :comments }, null: false, index: true
      t.bigint :child_comment_id, null: false

      t.timestamps
    end

    add_foreign_key :comments_relations, :comments, column: :parent_comment_id
  end
end
