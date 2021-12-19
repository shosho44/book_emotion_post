class PassagesCommentRelation < ApplicationRecord
  belongs_to :passage
  belongs_to :comment
end
