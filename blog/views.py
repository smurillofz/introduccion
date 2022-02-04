from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import View, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import PostCreateForm

from .models import Post
# Create your views here.
class BlogListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all();
        context={
            'posts':posts
        }
        return render(request, 'blog_list.html', context)

class BlogCreateView(View):
    def get(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST)
        context={
            'form':form
        }
        return render(request, 'blog_create.html', context)


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PostCreateForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                p, created = Post.objects.get_or_create(title=title, content=content)
                p.save()

                return redirect('blog:home')
        context={
        }
        return render(request, 'blog_create.html', context)

class ViewBlogDetail(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        context={
            'post':post
        }
        return render(request, 'blog_detail.html', context)

class BlogUpdate(UpdateView):
    model = Post #model
    fields = ['title','content'] # fields / if you want to select all fields, use "__all__"
    template_name = 'blog_update.html' # templete for updating

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('blog:detail', kwargs={'pk':pk})

class BlogDeleteView(DeleteView):
    model=Post
    template_name='blog_delete.html'
    success_url=reverse_lazy('blog:home')