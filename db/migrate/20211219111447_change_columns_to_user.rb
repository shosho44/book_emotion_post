class ChangeColumnsToUser < ActiveRecord::Migration[6.1]
  def change
    change_column :users, :id, :string, null: false, primary_key: true, index: true
    remove_column :users, :user_id
    change_column :users, :name, :string, null: false
    change_column :users, :email, :string, null: false
    change_column :users, :password_digest, :string, null: false
  end
end
