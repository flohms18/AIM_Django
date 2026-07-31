import plotly.graph_objects as go
from django.shortcuts import render

# Create your views here.

def index(request):
    fig = go.Figure(go.Bar(
        x=[20, 14, 23],
        y=['giraffes', 'orangutans', 'monkeys'],
        orientation='h'))

    plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render(request, 'index.html', {'plot_div': plot_div})
