import plotly.graph_objs as go
import plotly
data = [
    go.Bar(
        x=['x1', 'x2', 'x3', 'x4'],
        y=[11, 13, 17, 19]
    )
]
 
layout = plotly.graph_objs.Layout(
    title='Bar-chart'
)
 
figure = plotly.graph_objs.Figure(
    data=data, layout=layout
)
 
plotly.offline.plot(
figure, filename='./templates/basic_bar_chart.html'
)
