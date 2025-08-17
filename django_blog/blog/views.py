from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile_view(request):
    return render(request, "blog/profile.html")

'''CRUD Views'''

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import  PostForm, RegisterForm
from .models import Post

# List all posts
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ['-published_date']

# View single post
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update a post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# Post by tag
from django.shortcuts import get_object_or_404
from taggit.models import Tag

class PostByTagListView(ListView):
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        # Get the tag based on the URL slug
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        # Return posts that have this tag
        return Post.objects.filter(tags__in=[self.tag])

    def get_context_data(self, **kwargs):
        # Add the tag to the context
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


'''Comment Views '''


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView, DeleteView


# Add comment to a post
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/add_comment.html"

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs.get('post_id')
        return reverse_lazy('post_detail', kwargs={'pk': post_id})

# Update comment
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

# Delete comment
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


# Search View
from django.db.models import Q

def post_search(request):
    query = request.GET.get('q')
    results = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
    ).distinct()
    return render(request, "blog/post_search.html", {"results": results, "query": query})
