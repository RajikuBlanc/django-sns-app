from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Post


class Home(LoginRequiredMixin, ListView):
    # 自分以外のユーザーの投稿を表示
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        return Post.objects.exclude(user=self.request.user)


class MyPost(LoginRequiredMixin, ListView):
    # 自分の投稿を表示
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class DetailPost(LoginRequiredMixin, DetailView):
    # 投稿の詳細を表示
    model = Post
    template_name = 'detail.html'
