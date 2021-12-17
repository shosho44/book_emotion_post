class Passage < ApplicationRecord
  validates :content, presence: true, length: { maximum: 1023 }

  validates :book_title, length: { maximum: 255 }

  VALID_USER_ID_REGEX = /[a-zA-Z0-9_-]+/
  validates :user_id, presence: true, length: { maximum: 255 }, format: { with: VALID_USER_ID_REGEX }
end
