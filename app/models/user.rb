class User < ApplicationRecord
  has_many :comments, dependent: :delete_all
  has_many :comment_likes, dependent: :delete_all
  has_many :passages, dependent: :delete_all
  has_many :passage_bookmarks, dependent: :delete_all

  attr_accessor :remember_token

  before_save { email.downcase! }
  VALID_EMAIL_REGEX = /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i
  validates :email, presence: true, length: { maximum: 255 }, format: { with: VALID_EMAIL_REGEX },
                    uniqueness: { case_sensitive: false }

  VALID_ID_REGEX = /[a-zA-Z0-9_-]+/
  validates :id, presence: true, length: { maximum: 255 }, format: { with: VALID_ID_REGEX }, uniqueness: true,
                 user_id_unprohibited: true

  has_secure_password
  validates :password, presence: true, length: { minimum: 6 }, allow_nil: true

  validates :name, presence: true, length: { maximum: 255 }

  def self.digest(string)
    cost = if ActiveModel::SecurePassword.min_cost
             BCrypt::Engine::MIN_COST
           else
             BCrypt::Engine.cost
           end
    BCrypt::Password.create(string, cost: cost)
  end

  def self.new_token
    SecureRandom.urlsafe_base64
  end

  def remember
    self.remember_token = User.new_token
    update_attribute(:remember_digest, User.digest(remember_token))
  end

  def authenticated?(remember_token)
    return false if remember_digest.nil?

    BCrypt::Password.new(remember_digest).is_password?(remember_token)
  end

  def forget
    update_attribute(:remember_digest, nil)
  end
end
