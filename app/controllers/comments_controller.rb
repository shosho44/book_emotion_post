class CommentsController < ApplicationController
  def show
    comment_id = params[:id].to_i

    @comment_form_model = Comment.new

    @comment = User.joins(:comments).where(comments: { id: comment_id }).select('users.name as user_name, comments.*').first

    @comment_likes = Comment.eager_load(:comment_likes).where(comments: { id: comment_id }).group('comments.id').count('comment_likes.id')[comment_id]

    comment_ids = CommentsRelation.where(parent_comment_id: comment_id).select('child_comment_id').map do |value|
      value.child_comment_id
    end

    @comments = User.joins(:comments)
                    .where('comments.id in (?)', comment_ids)
                    .select('users.id as user_id, users.name as user_name, comments.content as content, comments.id as id')
                    .order('comments.created_at desc').order('comments.user_id asc')

    @comments_likes = Comment.joins(:passages_comment_relation).eager_load(:comment_likes)
                             .where(passages_comment_relations: { passage_id: comment_id }).group('comments.id').count('comment_likes.id')
  end

  def create
    @comment = Comment.new(comment_params)
    @comment.save!

    if /passages/.match(request.referer)
      passage_id = %r{passages/([0-9]+)}.match(request.referer)[1].to_i

      @passage_comment_relation = PassagesCommentRelation.new(passage_id: passage_id, comment_id: @comment.id)
      @passage_comment_relation.save
    else
      parent_comment_id = %r{comments/([0-9]+)}.match(request.referer)[1].to_i

      @comments_relation = CommentsRelation.new(parent_comment_id: parent_comment_id, child_comment_id: @comment.id)
      @comments_relation.save
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
