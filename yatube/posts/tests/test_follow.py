from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Group, Post, Follow

User = get_user_model()


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Текст поста',
            author=cls.user,
            group=cls.group,
            pub_date='Дата публикации',

        )
        cls.followers = 'Тестовый Пользователь который подписывается'
        cls.followings = 'Тестовый Пользователь на которого подписываются'

    def setUp(self):
        self.guest_client = Client()
        self.author_post = Client()
        self.author_post.force_login(self.user)
        self.authorized_user = User.objects.create_user(username='НЕ АВТОР')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.authorized_user)
        self.followers = Client()
        self.followings = Client()

    def test_profile_follow(self):
        """Авторизованный пользователь может подписываться
        на других пользователей """
        self.authorized_client.get(reverse('posts:profile_follow',
                                                      kwargs={'username': self.user}))
        self.assertEqual(Follow.objects.all().count(), 1)





    def test_profile_unfollow(self):
        """Авторизованный пользователь может удалять их из подписок"""
        response = self.authorized_client.get(reverse('posts:profile_unfollow',
                                                      kwargs={'username': self.user}))

        self.assertRedirects(response, (f'/profile/{self.user}/'))

