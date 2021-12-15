class UsersController < ApplicationController
  def new
    @user = User.new
  end

  def show
    @user = User.find_by(user_id: params[:id])
  end

  def create
    @user = User.new(params[:user])
    if @user.save
      redirect_to root_url
    else
      render 'new'
    end
  end

  def updated
    @user = User.find(params[:id])
  end

  def edit
    @user = User.find(params[:id])
  end

  def destroy
    @user.destroy
  end

  # TODO: 変更する必要あり
  def user_params
    params.require(:user).permit(:user_id, :name, :email, :password, :password_confirmation)
  end
end
