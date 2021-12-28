class CommentsController < ApplicationController
  def show
    @comment_form_model = Comment.new

    @comment = User.joins(:comments).where(comments: { id: params[:id] }).select('users.name as user_name, comments.*').first

    @comment_like = Comment.eager_load(:comment_likes).where(comments: { id: params[:id] }).group('comments.id').count('comment_likes.id').map do |_key, value|
      value
    end

    @comments = User.joins(:comments).eager_load(comments: :comments_relations).eager_load(comments: :comment_likes)
                    .where(comments_relations: { parent_comment_id: 1 })
                    .select('users.id as user_id, users.name as user_name, comments.content as content, comments.id as id')
                    .order('comments.created_at desc').order('comments.user_id asc')

    @comments_likes = Comment.joins(:passages_comment_relation).eager_load(:comment_likes)
                             .where(passages_comment_relations: { passage_id: 1 }).group('comments.id').count('comment_likes.id')
  end

  def create
    @comment = Comment.new(comment_params)
    @comment.save

    if /passages/.match(request.referer)
      passage_id = %r{passages/([0-9]+)}.match(request.referer)[1]

      @passage_comment_relation = PassagesCommentRelation.new(passage_id: passage_id, comment_id: @comment.id)
      @passage_comment_relation.save
    end

    redirect_to request.referer
  end

  def destroy
    @comment = Comment.find(params[:id])
    @comment.destroy
    redirect_to request.referer
  end

  private

  def comment_params
    params.require(:comment).permit(:content).merge(user_id: params[:user_id])
  end
end
