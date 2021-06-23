class SystemConfig:
    POST_ARTICLE_DATABASE_URI = 'sqlite:///db.post_article'
    
    SQLALCHEMY_DATABASE_URI = POST_ARTICLE_DATABASE_URI


Config = SystemConfig
