class PassageBookmark < ApplicationRecord
  belongs_to :user
  belongs_to :passage
end
