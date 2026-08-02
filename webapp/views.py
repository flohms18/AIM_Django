import plotly.graph_objects as go
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags

from .models import Post, GlossaryTerm, Tag, Category

POSTS_PER_PAGE = 5

# Create your views here.


def _reading_time(post):
    word_count = len(strip_tags(post.content).split())
    return max(1, round(word_count / 200))


def index(request):
    topics = (
        Tag.objects.annotate(num_posts=Count('posts'))
        .filter(num_posts__gt=0)
        .order_by('num_posts')
    )
    labels = [tag.name for tag in topics]
    values = [tag.num_posts for tag in topics]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker=dict(color='#5c6bff', cornerradius=6, line=dict(width=0)),
        hovertemplate='%{y} : %{x}<extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9ca3af', family='ui-sans-serif, system-ui, sans-serif', size=12),
        margin=dict(l=0, r=30, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(showgrid=False, autorange='reversed', color='#e5e7eb', ticklabelstandoff=10),
        bargap=0.45,
        height=260,
        annotations=[
            dict(
                x=value,
                y=label,
                text=str(value),
                showarrow=False,
                xshift=15,       # gap in pixels between bar end and text
                xanchor='left',
            )
            for label, value in zip(labels, values)
        ],
    )

    topics_chart = fig.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config={'displayModeBar': False, 'responsive': True},
    )

    posts = Post.objects.order_by('-published_date')
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    for post in page_obj:
        post.reading_time = _reading_time(post)

    overview_stats = {
        'articles': Post.objects.count(),
        'glossary_terms': GlossaryTerm.objects.count(),
        'modules': Post.objects.filter(types__name__icontains='module').distinct().count(),
        'datastories': Post.objects.filter(types__name__icontains='datastor').distinct().count(),
    }

    return render(request, 'index.html', {
        'topics_chart': topics_chart,
        'page_obj': page_obj,
        'overview_stats': overview_stats,
    })


def article(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.reading_time = _reading_time(post)

    related_posts = Post.objects.exclude(pk=post.pk).order_by('-published_date')[:3]
    for related in related_posts:
        related.reading_time = _reading_time(related)

    return render(request, 'article.html', {'post': post, 'related_posts': related_posts})


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    posts = Post.objects.filter(category=category).order_by('-published_date')
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    for post in page_obj:
        post.reading_time = _reading_time(post)

    return render(request, 'category.html', {'category': category, 'page_obj': page_obj})


def lexique(request):
    terms = GlossaryTerm.objects.order_by('term')
    return render(request, 'lexique.html', {'terms': terms})
