class PassagesController < ApplicationController
  def create
    puts passage_params
    @passage = Passage.new(passage_params)
    @passage.save
    redirect_to root_url
  end

  def show
    @passage = Passage.find(params[:id])
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
