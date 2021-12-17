class CreatePassages < ActiveRecord::Migration[6.1]
  def change
    create_table :passages do |t|
      t.integer :user_id
      t.string :book_title
      t.string :content

      t.timestamps
    end
  end
end
