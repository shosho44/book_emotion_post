class SystemConfig:
    POST_ARTICLE_DATABASE_URI = 'sqlite:///db.post_article'
    USER_INFORMATION_DATABASE_URI = 'sqlite:///db.user_information'
    
    SQLALCHEMY_BINDS = {"post_article_db": POST_ARTICLE_DATABASE_URI, "user_information_db": USER_INFORMATION_DATABASE_URI}


Config = SystemConfig
