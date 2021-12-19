class CommentsController < ApplicationController
  def show
    @comment = Comment.find(params[:id])
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
