class Comment < ApplicationRecord
  belongs_to :user
  has_one :passages_comment_relation, dependent: :destroy
  has_many :comment_likes, dependent: :delete_all
  has_many :comments_relations, foreign_key: 'parent_comment_id', dependent: :delete_all
end
