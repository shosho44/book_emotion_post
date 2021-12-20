User.create!(id: 'test_user_1', name: 'test_user1', email: 'test1@test.user', self_introduction: '私はテストユーザー1です',
             password: 'asdfawref34t5yhesxd')
User.create!(id: 'test_user_2', name: 'test_user2', email: 'test2@test.user',
             password: 'asdfawref34t5yhesxd')

Passage.create!(book_title: 'test1', content: 'test1', user_id: 'test_user_1')
Passage.create!(book_title: 'test2', content: 'test2', user_id: 'test_user_2')
Passage.create!(book_title: 'test3', content: 'test3', user_id: 'test_user_1')
Passage.create!(book_title: 'test4', content: 'test4', user_id: 'test_user_2')

Comment.create!(content: 'test1', user_id: 'test_user_1')
Comment.create!(content: 'test2', user_id: 'test_user_2')

PassagesCommentRelation.create!(passage_id: 1, comment_id: 1)
PassagesCommentRelation.create!(passage_id: 1, comment_id: 2)
