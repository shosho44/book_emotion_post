# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2021_12_28_141730) do

  create_table "comment_likes", charset: "utf8mb3", force: :cascade do |t|
    t.string "user_id", null: false
    t.bigint "comment_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["comment_id"], name: "index_comment_likes_on_comment_id"
    t.index ["user_id"], name: "index_comment_likes_on_user_id"
  end

  create_table "comments", charset: "utf8mb3", force: :cascade do |t|
    t.string "user_id", null: false
    t.text "content", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["id"], name: "index_comments_on_id", unique: true
    t.index ["user_id"], name: "index_comments_on_user_id"
  end

  create_table "comments_relations", charset: "utf8mb3", force: :cascade do |t|
    t.bigint "parent_comment_id", null: false
    t.bigint "child_comment_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["parent_comment_id"], name: "index_comments_relations_on_parent_comment_id"
  end

  create_table "passage_bookmarks", charset: "utf8mb3", force: :cascade do |t|
    t.string "user_id", null: false
    t.bigint "passage_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["passage_id"], name: "index_passage_bookmarks_on_passage_id"
    t.index ["user_id"], name: "index_passage_bookmarks_on_user_id"
  end

  create_table "passages", charset: "utf8mb3", force: :cascade do |t|
    t.string "user_id", null: false
    t.string "book_title", default: "", null: false
    t.text "content", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["id"], name: "index_passages_on_id", unique: true
    t.index ["user_id"], name: "index_passages_on_user_id"
  end

  create_table "passages_comment_relations", charset: "utf8mb3", force: :cascade do |t|
    t.bigint "passage_id", null: false
    t.bigint "comment_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["comment_id"], name: "index_passages_comment_relations_on_comment_id"
    t.index ["passage_id"], name: "index_passages_comment_relations_on_passage_id"
  end

  create_table "users", id: :string, charset: "utf8mb3", force: :cascade do |t|
    t.string "name", null: false
    t.string "email", null: false
    t.string "self_introduction"
    t.string "password_digest", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["id"], name: "index_users_on_id", unique: true
  end

  add_foreign_key "comment_likes", "comments"
  add_foreign_key "comment_likes", "users"
  add_foreign_key "comments", "users"
  add_foreign_key "comments_relations", "comments", column: "parent_comment_id"
  add_foreign_key "passage_bookmarks", "passages"
  add_foreign_key "passage_bookmarks", "users"
  add_foreign_key "passages", "users"
  add_foreign_key "passages_comment_relations", "comments"
  add_foreign_key "passages_comment_relations", "passages"
end
