class UserIdUnprohibitedValidator < ActiveModel::EachValidator
  def validate_each(record, attribute, value)
    prohibited_user_id = ['unauthenticated_user']

    record.errors[attribute] << (options[:message] || '使えないユーザーidです') if prohibited_user_id.include?(value)
  end
end
