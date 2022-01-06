class CookiesController < ApplicationController
  def new; end

  def create
    user = User.find(params[:id])

    if user
      user.remember
      log_in(user)
      redirect_to root_url
    else
      redirect_to login_path
    end
  end

  def log_out; end

  def destroy
    user = User.find(params[:id])
    log_out(user) if logged_in?
    redirect_to login_path
  end
end
