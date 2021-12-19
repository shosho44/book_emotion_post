class Comment < ApplicationRecord
  belongs_to :user
  has_one :passage_comment_relation
end
