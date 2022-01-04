class CreateCommentLikes < ActiveRecord::Migration[6.1]
  def change
    create_table :comment_likes do |t|
      t.string :user_id, foreign_key: true, null: false, index: true
      t.bigint :comment_id, foreign_key: true, null: false, index: true
      t.timestamps
    end

    add_foreign_key :comment_likes, :users
    add_foreign_key :comment_likes, :comments
  end
end
