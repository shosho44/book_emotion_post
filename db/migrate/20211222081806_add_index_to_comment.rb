class AddIndexToComment < ActiveRecord::Migration[6.1]
  def change
    add_index :comments, :id
  end
end
