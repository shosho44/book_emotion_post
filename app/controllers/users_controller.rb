class UsersController < ApplicationController
  def new
    @user = User.new
  end

  def show
    @user = User.find(params[:id])
  end

  def create
    @user = User.new(user_params)
    if @user.save
      redirect_to root_url
    else
      render 'new'
    end
  end

  def update_name_self_introduction
    @user = User.find(params[:id])
    if @user.update(user_name_self_introduction_params)
      redirect_to @user
    else
      render 'edit'
    end
  end

  def edit
    @user = User.find(params[:id])
  end

  def destroy
    @user.destroy
  end

  # TODO: 変更する必要あり
  def user_params
    params.require(:user).permit(:id, :name, :email, :password, :password_confirmation)
  end

  def user_name_self_introduction_params
    params.require(:user).permit(:name, :self_introduction)
  end
end
