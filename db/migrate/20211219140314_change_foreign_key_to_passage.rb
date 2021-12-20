class ChangeForeignKeyToPassage < ActiveRecord::Migration[6.1]
  def change
    remove_column :passages, :user_id
    add_reference :passages, :user, type: :string, null: false, foreign_key: true
    change_column :passages, :book_title, :string, null: false, default: '不明'
    change_column :passages, :content, :text, null: false
  end

  add_foreign_key :passages, :users
end
