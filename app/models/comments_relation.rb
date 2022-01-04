class CommentsRelation < ApplicationRecord
  belongs_to :comment, foreign_key: 'parent_comment_id'
end
