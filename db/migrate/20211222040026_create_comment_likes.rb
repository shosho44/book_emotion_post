class CreateCommentLikes < ActiveRecord::Migration[6.1]
  def change
    create_table :comment_likes do |t|
      t.string :user_id, foreign_key: { to_table: :users }, null: false, index: true
      t.references :comment, foreign_key: { to_table: :comments }, null: false, index: true
      t.timestamps
    end
  end
end
