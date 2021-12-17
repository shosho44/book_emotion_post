Rails.application.routes.draw do
  root 'passages#show'

  resources :users, path_names: { new: 'signup' } do
    resource :bookmarks, { only: %i[show] } # TODO: bookmarks用のコントローラ作成
    resources :passages, { only: %i[create destroy] }
  end

  patch 'users/:id/update-name-self-introduction', to: 'users#update_name_self_introduction'
end
