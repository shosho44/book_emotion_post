Rails.application.routes.draw do
  resources :users do
    resource :bookmarks, { only: %i[show] } # TODO: bookmarks用のコントローラ作成
  end
end
