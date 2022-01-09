class CookiesController < ApplicationController
  include ApplicationHelper

  def new; end

  def create
    user = User.find_by(id: params[:id])

    if user&.authenticate(params[:password])
      user.remember
      log_in(user)
      redirect_to root_url
    else
      redirect_to login_path
    end
  end

  def show_log_out; end

  def destroy
    user = User.find_by(id: current_user.id)
    log_out(user) if logged_in?
    redirect_to login_path
  end
end
