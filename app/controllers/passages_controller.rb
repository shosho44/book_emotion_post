class PassagesController < ApplicationController
  def create
    @passage = Passage.new(passage_params)
    @passage.save
    redirect_to root_url
  end

  def show
    @passage = User.joins(:passages).where(passages: { id: params[:id] }).select('users.name as user_name, passages.*').first
    @passage_bookmarks = Passage.joins(:passage_bookmarks).where(passages: { id: params[:id] }).count

    @comment = Comment.new
    @comments = User.joins(passages: :comments).where(passages: { id: params[:id] })
                    .select('users.id as user_id, users.name as user_name, comments.content as content, comments.id as id, passages.content as passge_content')
                    .order('comments.created_at desc').order('comments.user_id asc')
    @comments_likes_plus_one = Passage.joins(:comments).includes(comments: :comment_likes).where(passages: { id: params[:id] }).order('comments.created_at desc').order('comments.user_id asc').group(:comment_id).count
    @comments_likes = @comments_likes_plus_one.map { |_key, value| value - 1 }
  end

  def show_all
    @passage = Passage.new
    @passages = User.joins(:passages).select('users.name as user_name, passages.*').order('passages.created_at desc').order('passages.user_id asc')
    @passages_bookmarks = Passage.eager_load(:passage_bookmarks)
                                 .select('passages.id as passage_id')
                                 .order('passages.created_at desc').order('passages.user_id asc')
                                 .group('passages.id')
                                 .count('passage_bookmarks.id').map { |_key, value| value }
  end

  def destroy
    @passage = Passage.find(params[:id])
    @passage.destroy
    redirect_to root_url
  end

  private

  def passage_params
    params.require(:passage).permit(:content, :book_title).merge(user_id: params[:user_id]) # TODO: current_userが出来たらcurrent_userのidを入れる
  end
end
