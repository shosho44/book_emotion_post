Rails.application.routes.draw do
  root 'passages#show_all'
  get 'users/:user_id/passages/:passage_id/bookmarks', to: 'bookmarks#show_passage_bookmarks'
  post 'users/:user_id/passages/:passage_id/bookmarks/check', to: 'bookmarks#try_create_bookmark'

  resources :users, path_names: { new: 'signup' } do
    resource :bookmarks, { only: %i[show] } # TODO: bookmarks用のコントローラ作成
    resources :passages, { only: %i[create destroy show] }
    resources :comments, { only: %i[create destroy show] }
  end

  patch 'users/:id/update-name-self-introduction', to: 'users#update_name_self_introduction'
end
