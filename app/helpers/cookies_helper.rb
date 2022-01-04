module CookiesHelper
  def log_in(user)
    cookies.permanent.signed[:user_id] = user.id
    cookies.permanent[:remember_token] = user.remember
  end

  def logged_in?
    !current_user.nil?
  end

  def log_out(current_user)
    current_user.forget
    cookies.delete(:user_id)
    cookies.delete(:remember_token)
    @current_user = nil
  end

  def current_user
    if (user_id = cookies.signed[:user_id])
      user = User.find(user_id)
      @current_user = user if user && user.authenticated?(cookies[:remember_token])
    end
  end
end
