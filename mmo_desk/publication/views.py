from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.db.models import Q
from django.shortcuts import render


class PostList(ListView):
    model = Post
    queryset = Post.objects.order_by('-date')
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_kind'] = 'Статьи'
        return context


def create_query_for_comment(user_id):
    post_list = Post.objects.filter(author_id=user_id).order_by('-date')
    comment_list = []
    for post in post_list:
        comments = Comment.objects.filter(post_id=post.pk).values('main_text', 'author_id', 'kind', 'id')
        for comment in comments:
            if comment['author_id'] != user_id:
                comment_list.append(comment)
    if comment_list:
        query = Q()
        for comm in comment_list:
            query |= Q(main_text=comm['main_text'], author_id=comm['author_id'], kind=comm['kind'], id=comm['id'])
        comment_queryset = Comment.objects.filter(query).select_related('author').values('main_text', 'author__username',
                                                                                         'kind', 'id')
    else:
        comment_queryset = []
    return comment_queryset


class MyPostList(PermissionRequiredMixin, ListView):
    permission_required = 'publication.view_post'
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        user_id = self.request.user.pk
        return create_query_for_comment(user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_name'] = self.request.user.username
        return context


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = User.objects.get(pk=Post.objects.get(pk=post_id).author_id)
    print('EMAIL', user.email)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author_id = request.user.id
            comment.save()

            subject = 'Вы получили новый отклик'
            html_message = render_to_string('mail/new_comment.html', {
                'user': user,
                'link': post_id,
                'comment': form.data['main_text'],
            })
            plain_message = strip_tags(html_message)
            from_email = 'help@psymphony.ru'
            to_email = user.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
    return redirect('post_detail', post_id=post_id)


def send_email_comment(comment_id, post_id):
    author = User.objects.get(pk=Comment.objects.get(pk=comment_id).author_id)
    subject = 'Ваш отклик принят!'
    html_message = render_to_string('mail/accept_comment.html', {
        'user': author,
        'link': post_id,
        'comment': Comment.objects.get(pk=comment_id).main_text,
    })
    plain_message = strip_tags(html_message)
    from_email = 'help@psymphony.ru'
    to_email = author.email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


def comment_change_kind(request, post_id, comment_id, kind):
    if kind == 1:
        Comment.objects.filter(pk=comment_id).update(kind='accept')
        send_email_comment(comment_id, post_id)
    else:
        Comment.objects.filter(pk=comment_id).update(kind='cancel')
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post_id=post_id).select_related('author').values('id', 'main_text', 'author__username', 'kind')
    form = CommentForm()
    user = request.user
    return render(request, 'publ.html', {'publ': post, 'comments': comments, 'form': form, 'user': user})


def comment_change_kind_from_mylist(request, comment_id, kind):
    post_id = Post.objects.get(pk=Comment.objects.get(pk=comment_id).post_id).id
    if kind == 1:
        Comment.objects.filter(pk=comment_id).update(kind='accept')
        send_email_comment(comment_id, post_id)
    else:
        Comment.objects.filter(pk=comment_id).update(kind='cancel')
    user = request.user
    return render(request, 'comments.html', {'comments': create_query_for_comment(user.id)})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post_id=post_id).select_related('author').values('id', 'main_text', 'author__username', 'kind')
    user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'publ.html', {'publ': post, 'comments': comments, 'form': form, 'user': user})


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'publication.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author_id = self.request.user.id
        self.object.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'publication.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author_id = self.request.user.id
        self.object.save()
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


