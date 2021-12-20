class ChangeColumnToPassage < ActiveRecord::Migration[6.1]
  def change
    change_column :passages, :user_id, :string, null: false
  end
end
