Rails.application.routes.draw do
  root 'passages#show_all'

  get 'login', to: 'cookies#new'
  resource :cookies, { only: %i[create destroy] }

  resources :users, path_names: { new: 'signup' } do
    resource :bookmarks, { only: %i[show] }

    resources :passages, { only: %i[create destroy show] } do
      get 'bookmarks', to: 'bookmarks#show_passage_bookmarks'
      post 'bookmarks/check', to: 'bookmarks#try_create_bookmark'
    end

    resources :comments, { only: %i[create destroy show] } do
      get 'likes', to: 'likes#show_comment_likes'
      post 'likes/check', to: 'likes#try_create_like'
    end
  end

  patch 'users/:id/update-name-self-introduction', to: 'users#update_name_self_introduction'
end
