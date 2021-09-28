from bukuemo import models

# bukuemo.models.initを行った後にtableが作成されているかの確認
def test_table_exists():
    try:
        models.Comments.query.all()
        print('models.Comments exists')
    except Exception as e:
        print('error: {}'.format(e))
    
    try:
        models.CommentLikes.query.all()
        print('models.CommentLikes exists')
    except Exception as e:
        print('error: {}'.format(e))
    
    try:
        models.Passages.query.all()
        print('models.Passages exists')
    except Exception as e:
        print('error: {}'.format(e))
    
    try:
        models.PostCommentRelations.query.all()
        print('models.PostCommentRelations exists')
    except Exception as e:
        print('error: {}'.format(e))
    
    try:
        models.PassageLikes.query.all()
        print('models.PassageLikes exists')
    except Exception as e:
        print('error: {}'.format(e))
    
    try:
        models.PostIDs.query.all()
        print('models.PostIDs exists')
    except Exception as e:
        print('error: {}'.format(e))
    
    try:
        models.UserLoginInformation.query.all()
        print('models.UserLoginInformation exists')
    except Exception as e:
        print('error: {}'.format(e))
    
    try:
        models.Users.query.all()
        print('models.Users exists')
    except Exception as e:
        print('error: {}'.format(e))