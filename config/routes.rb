Rails.application.routes.draw do
  resources :users, path_names: { new: 'signup' } do
    resource :bookmarks, { only: %i[show] } # TODO: bookmarks用のコントローラ作成
  end
end
