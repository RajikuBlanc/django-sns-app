from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView,CreateView
from django.urls import reverse_lazy
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

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create.html'
    fields = ['title','content','image']
    success_url = reverse_lazy('mypost')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
