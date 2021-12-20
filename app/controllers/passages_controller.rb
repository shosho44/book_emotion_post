class PassagesController < ApplicationController
  def create
    @passage = Passage.new(passage_params)
    @passage.save
    redirect_to root_url
  end

  def show
    @passage = Passage.find(params[:id])
    @comment = Comment.new
    @comments = Passage.joins(passages_comment_relations: :comment).select('comments.*').where(passages: { id: params[:id] }).order('comments.created_at desc').order('comments.user_id asc')
  end

  def show_all
    @passage = Passage.new
    @passages = Passage.all.order(created_at: :desc).order(user_id: :asc)
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
