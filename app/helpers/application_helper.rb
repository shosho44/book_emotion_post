module ApplicationHelper
  def log_in(user)
    cookies.permanent.signed[:user_id] = user.id
    cookies.permanent[:remember_token] = user.remember_token
    user
  end

  def logged_in?
    !current_user.id.eql?('unauthenticated_user')
  end

  def log_out(current_user)
    current_user.forget
    cookies.delete(:user_id)
    cookies.delete(:remember_token)
  end

  def current_user
    user_id = cookies.signed[:user_id]
    if !user_id
      User.new(id: 'unauthenticated_user')
    else
      user = User.find(user_id)
      user if user && user.authenticated?(cookies[:remember_token])
    end
  end
end
