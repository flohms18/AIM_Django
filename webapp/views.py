import plotly.graph_objects as go
from django.shortcuts import render

# Create your views here.

# TODO: remplacer par les vraies données une fois disponibles.
TOPICS = [
    ("Generative AI", 7),
    ("Data Engineering", 8),
    ("RAG & Fine-tuning", 9),
    ("Transformers & NLP", 10),
    ("Data Governance", 12),
    ("LLMs", 15),
]


def index(request):
    labels = [label for label, _ in TOPICS]
    values = [value for _, value in TOPICS]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker=dict(color='#5c6bff', cornerradius=6),
        text=values,
        textposition='outside',
        hovertemplate='%{y} : %{x}<extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9ca3af', family='ui-sans-serif, system-ui, sans-serif', size=12),
        margin=dict(l=0, r=30, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(showgrid=False, autorange='reversed', color='#e5e7eb'),
        bargap=0.45,
        height=260,
    )

    topics_chart = fig.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config={'displayModeBar': False, 'responsive': True},
    )

    return render(request, 'index.html', {'topics_chart': topics_chart})
