class UsersController < ApplicationController
  include ApplicationHelper

  def new
    @user = User.new
  end

  def show
    @user = User.find_by(id: params[:id])

    @passages = User.joins(:passages).where(users: { id: params[:id] }).select('users.name as user_name, passages.*')
                    .order('passages.created_at desc').order('passages.user_id asc')

    @passages_bookmarks = Passage.eager_load(:passage_bookmarks).where(passages: { user_id: params[:id] })
                                 .select('passages.id as passage_id').order('passages.created_at desc').order('passages.user_id asc')
                                 .group('passages.id').count('passage_bookmarks.id').map { |_key, value| value }
  end

  def create
    user = User.new(user_params)
    if user.save
      user.remember
      log_in(user)
      redirect_to root_url
    else
      render 'new'
    end
  end

  def update_name_self_introduction
    @user = User.find_by(id: params[:id])
    if @user.update(user_name_self_introduction_params)
      redirect_to @user
    else
      render 'edit'
    end
  end

  def edit
    @user = User.find_by(id: params[:id])
  end

  def destroy
    @user.destroy
  end

  private

  def user_params
    params.require(:user).permit(:id, :name, :email, :password, :password_confirmation)
  end

  def user_name_self_introduction_params
    params.require(:user).permit(:name, :self_introduction)
  end
end
