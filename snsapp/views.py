from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.views import View
from django.urls import reverse_lazy
from .models import Post,Connection


class Home(LoginRequiredMixin, ListView):
    # 自分以外のユーザーの投稿を表示
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        return Post.objects.exclude(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #get_or_createにしないとサインアップ時オブジェクトがないためエラーになる
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context


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
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create.html'
    fields = ['title','content','image']
    success_url = reverse_lazy('mypost')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdatePost(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    # 特定のユーザーだけが編集できるようにUserPassesTestMixinを使用する
    model = Post
    template_name = "update.html"
    fields = ['title','content','image']
    success_url = reverse_lazy('mypost')

    # 編集後の遷移先をdetailにしたい場合はpkが必要（どの投稿かを特定するため）
    # そのため、get_success_urlを使用する必要がある
    # def get_success_url(self,**kwargs):
    #     pk = self.kwargs["pk"]
    #     return reverse_lazy('mypost')

    # アクセスできるユーザーを制限
    def test_func(self,**kwargs):
        pk = self.kwargs["pk"]
        # 投稿を特定するためにpkが必要
        post  = Post.objects.get(pk=pk)
        # 投稿者とリクエストユーザーが一致した場合のみ編集可能にする
        return (post.user == self.request.user)

class DeletePost(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = "delete.html"
    success_url = reverse_lazy('mypost')

    # アクセスできるユーザーを制限
    def test_func(self,**kwargs):
        pk = self.kwargs["pk"]
        post  = Post.objects.get(pk=pk)
        return (post.user == self.request.user)

class LikeBase(LoginRequiredMixin,View):
    def get(self,request, *args, **kwargs):
        pk = self.kwargs["pk"]
        related_post = Post.objects.get(pk=pk)

        if self.request.user in related_post.like.all():
            obj = related_post.like.remove(self.request.user)
        else:
            obj = related_post.like.add(self.request.user)
        return obj

class LikeHome(LikeBase):
    def get(self,request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('home')

class LikeDetail(LikeBase):
    def get(self,request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs["pk"]
        return redirect('detail' ,pk)


class FollowBase(LoginRequiredMixin, View):
    """フォローのベース。リダイレクト先を以降で継承先で設定"""
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        target_user = Post.objects.get(pk=pk).user

        my_connection = Connection.objects.get_or_create(user=self.request.user)

        if target_user in my_connection[0].following.all():
            obj = my_connection[0].following.remove(target_user)
        else:
            obj = my_connection[0].following.add(target_user)
        return obj

class FollowHome(FollowBase):
    """HOMEページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('home')

class FollowDetail(FollowBase):
    """詳細ページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        return redirect('detail', pk)

class FollowList(LoginRequiredMixin, ListView):
    """フォローしたユーザーの投稿をリスト表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        """フォローリスト内にユーザーが含まれている場合のみクエリセット返す"""
        my_connection = Connection.objects.get_or_create(user=self.request.user)
        all_follow = my_connection[0].following.all()
        return Post.objects.filter(user__in=all_follow)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context
