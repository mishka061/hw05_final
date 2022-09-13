
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Group, Post

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

    def setUp(self):
        self.guest_client = Client()
        self.author_post = Client()
        self.author_post.force_login(self.user)
        self.authorized_user = User.objects.create_user(username='НЕ АВТОР')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.authorized_user)
        self.followers_client = User.objects.create_user(username='Кто подписывается')
        self.followings_client = User.objects.create_user(username='На кого подписываются')



    def test_profile_follow(self):
        """Авторизованный пользователь может подписываться
        на других пользователей """
        response = self.authorized_client.get(reverse('posts:profile_follow',
                                                      kwargs={'username': self.user}))
        self.assertRedirects(response, (f'/profile/{self.user}/'))


    def test_profile_unfollow(self):
        """Авторизованный пользователь может удалять их из подписок"""
        response = self.authorized_client.get(reverse('posts:profile_unfollow',
                                                      kwargs={'username': self.user}))
        self.assertRedirects(response, (f'/profile/{self.user}/'))



