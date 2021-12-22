class Comment < ApplicationRecord
  belongs_to :user
  has_one :passages_comment_relation
  has_many :comment_likes
  has_many :comments_relations
end
