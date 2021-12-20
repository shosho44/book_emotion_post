class Comment < ApplicationRecord
  belongs_to :user
  has_one :passages_comment_relation
end
