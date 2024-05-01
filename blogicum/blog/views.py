from django.shortcuts import render

from .models import Post, Category

POSTS_PER_PAGE = 5


def index(request):
    post_list = Post.objects.post_published()[:POSTS_PER_PAGE]

    context = {
        'post_list': post_list
    }

    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = Post.objects.get_published_post(id)

    context = {
        'post': post
    }

    return render(request, 'blog/detail.html', context)


def category_posts(request, slug):
    category = Category.objects.category_post(slug)
    post_list = category.post_set.post_published()

    context = {
        'category': category,
        'post_list': post_list,
    }

    return render(request, 'blog/category.html', context)
