class ChangeColumnsToComment < ActiveRecord::Migration[6.1]
  def change
    remove_column :comments, :user_id
    add_reference :comments, :user, type: :string, null: false, foreign_key: true
    change_column :comments, :content, :text, null: false
  end

  add_foreign_key :comments, :users
end
