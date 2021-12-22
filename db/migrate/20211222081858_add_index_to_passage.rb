class AddIndexToPassage < ActiveRecord::Migration[6.1]
  def change
    add_index :passages, :id
  end
end
