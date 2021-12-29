class CreateUsers < ActiveRecord::Migration[6.1]
  def change
    create_table :users, id: :string do |t|
      t.string :name, null: false
      t.string :email, null: false
      t.string :self_introduction
      t.string :password_digest, null: false

      t.timestamps
    end

    add_index :users, :id, unique: true
  end
end
