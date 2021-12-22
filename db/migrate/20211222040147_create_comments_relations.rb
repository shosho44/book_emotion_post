class CreateCommentsRelations < ActiveRecord::Migration[6.1]
  def change
    create_table :comments_relations do |t|
      t.references :parent_comment, foreign_key: { to_table: :comments }, null: false, index: true
      t.references :child_comment, foreign_key: { to_table: :comments }, null: false, index: true

      t.timestamps
    end
  end
end
