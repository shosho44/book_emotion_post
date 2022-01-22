class PassagesController < ApplicationController
  include ApplicationHelper

  def create
    @passage = Passage.new(passage_params)

    @passage.book_title = '不明' if @passage.book_title == ''

    @passage.save

    redirect_to root_url
  end

  def show
    passage_id = params[:id].to_i

    @passage = User.joins(:passages).where(passages: { id: passage_id }).select('users.name as user_name, passages.*').first
    @passage_bookmarks = Passage.eager_load(:passage_bookmarks).where(passages: { id: passage_id }).group('passages.id').count('passage_bookmarks.id')[passage_id]

    @comment_form_model = Comment.new
    @comments = User.joins(comments: :passages_comment_relation).where(passages_comment_relations: { passage_id: passage_id })
                    .select('users.id as user_id, users.name as user_name, comments.content as content, comments.id as id')
                    .order('comments.created_at desc').order('comments.user_id asc')

    @comments_likes = Passage.joins(:comments).eager_load(comments: :comment_likes).where(passages: { id: passage_id })
                             .group('comments.id').count('comment_likes.id')

    @current_user = current_user
  end

  def show_all
    @passage = Passage.new
    @passages = User.joins(:passages).select('users.name as user_name, passages.*').order('passages.created_at desc').order('passages.user_id asc')
    @passages_bookmarks = Passage.eager_load(:passage_bookmarks)
                                 .select('passages.id as passage_id')
                                 .order('passages.created_at desc').order('passages.user_id asc')
                                 .group('passages.id')
                                 .count('passage_bookmarks.id').map { |_key, value| value }

    @current_user = current_user

    @has_user_logged_in = logged_in?
  end

  def destroy
    @passage = Passage.find_by(id: params[:id])
    @passage.destroy!
    redirect_to root_url
  end

  private

  def passage_params
    params.require(:passage).permit(:content, :book_title).merge(user_id: current_user.id)
  end
end
