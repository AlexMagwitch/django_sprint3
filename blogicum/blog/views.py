from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import Http404

from .models import Post, Category, Location


def index(request):
    current_time = timezone.now()

    post_list = Post.objects.filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]

    context = {
        'post_list': post_list
    }

    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    try:
        post = Post.objects.get(id=id)

        if (post.pub_date > timezone.now()
           or not post.is_published or not post.category.is_published):
            raise Http404("Страница не найдена")
        context = {
            'post': post,
        }

        return render(request, 'blog/detail.html', context)
    except Post.DoesNotExist:
        raise Http404("Страница не найдена")


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if not category.is_published:
        raise Http404("Страница не найдена")
    post_list = category.post_set.filter(
        is_published=True, pub_date__lte=timezone.now()).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list,
    }

    return render(request, 'blog/category.html', context)
