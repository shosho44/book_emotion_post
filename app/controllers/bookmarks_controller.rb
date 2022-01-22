class BookmarksController < ApplicationController
  include ApplicationHelper

  def show_passage_bookmarks
    @current_user = current_user

    @users_pushed_passage_bookmark = User.eager_load(:passage_bookmarks).where(passage_bookmarks: { passage_id: params[:passage_id] })
                                         .select('passage_bookmarks.user_id as user_id, users.name as name')
                                         .order('users.id asc')
  end

  def show; end

  def try_create_bookmark
    user_id_pushed_bookmark_button = params[:user_id]
    passage_id = params[:passage_id].to_i

    is_bookmark = !!PassageBookmark.find_by(user_id: user_id_pushed_bookmark_button, passage_id: passage_id)
    if is_bookmark
      destroy(user_id_pushed_bookmark_button, passage_id, request)
    else
      create(user_id_pushed_bookmark_button, passage_id, request)
    end
  end

  def create(user_id, passage_id, request)
    passage_bookmark = PassageBookmark.new(user_id: user_id, passage_id: passage_id)
    passage_bookmark.save

    redirect_to request.referer
  end

  def destroy(user_id, passage_id, request)
    passage_bookmark = PassageBookmark.find_by(user_id: user_id, passage_id: passage_id)
    passage_bookmark.destroy

    redirect_to request.referer
  end
end
