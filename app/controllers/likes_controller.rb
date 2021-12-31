class LikesController < ApplicationController
  def show_comment_likes
    @users_pushed_comment_like = User.eager_load(:comment_likes).where(comment_likes: { comment_id: params[:comment_id] })
                                     .select('comment_likes.user_id as user_id, users.name as name')
                                     .order('users.id asc')
  end

  def try_create_like
    user_id_pushed_like_button = params[:user_id]
    comment_id = params[:comment_id].to_i

    is_like = !!CommentLike.find_by(user_id: user_id_pushed_like_button, comment_id: comment_id)
    if is_like
      destroy(user_id_pushed_like_button, comment_id, request)
    else
      create(user_id_pushed_like_button, comment_id, request)
    end
  end

  def create(user_id, comment_id, request)
    comment_like = CommentLike.new(user_id: user_id, comment_id: comment_id)
    comment_like.save

    redirect_to request.referer
  end

  def destroy(user_id, comment_id, request)
    comment_like = CommentLike.find_by(user_id: user_id, comment_id: comment_id)
    comment_like.destroy

    redirect_to request.referer
  end
end
