class UsersController < ApplicationController
  def new
    @user = User.new
  end

  def show
    @user = User.find(params[:id])
    @passages = User.joins(:passages).where(users: { id: params[:id] }).select('users.name as user_name, passages.*').order('passages.created_at desc').order('passages.user_id asc')
    @passages_bookmarks_plus_one = Passage.includes(:passage_bookmarks).order('passages.created_at desc').order('passages.user_id asc').group('passages.id').count
    @passages_bookmarks = @passages_bookmarks_plus_one.map { |_key, value| value - 1 }
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

  private

  def user_params
    params.require(:user).permit(:id, :name, :email, :password, :password_confirmation)
  end

  def user_name_self_introduction_params
    params.require(:user).permit(:name, :self_introduction)
  end
end
