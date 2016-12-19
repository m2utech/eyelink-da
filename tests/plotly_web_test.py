# Get this figure: fig = py.get_figure("https://plot.ly/~empet/6640/")
# Get this figure's data: data = py.get_figure("https://plot.ly/~empet/6640/").get_data()
# Add data to this figure: py.plot(Data([Scatter(x=[1, 2], y=[2, 3])]), filename ="Nobel-women", fileopt="extend")
# Get y data of first trace: y1 = py.get_figure("https://plot.ly/~empet/6640/").get_data()[0]["y"]

# Get figure documentation: https://plot.ly/python/get-requests/
# Add data documentation: https://plot.ly/python/file-options/

# If you're using unicode in your file, you may need to specify the encoding.
# You can reproduce this figure in Python with the following code!

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('eddkkang', 'nsVN0W8K1BZQXZTQ4mSn')
trace1 = {
  "x": [3.29693424735, 4.33455523647, 4.65040429982, 0.477869009817, -1.33130293555, -0.188025259484, 1.66370024197, 1.02982145369, 3.28802725247, 0.961057306456, -2.80881942552, -0.341682748294, 1.98287719166, 4.23980230417, -0.545342393077, 1.28230999383], 
  "y": [-0.29759475972, 1.0, -0.198044948645, -1.79910803293, -4.25480056731, 3.36775100177, -4.54263081373, -0.966628092125, -1.32328918, -3.25344177367, -0.71396182408, -2.83519217957, -2.59617523687, -1.57223251086, 1.47409107521, 1.65742045032], 
  "hoverinfo": "text", 
  "marker": {
    "color": "#74f2b8", 
    "line": {
      "color": "#000000", 
      "width": 0.5
    }, 
    "size": 20, 
    "symbol": "dot"
  }, 
  "mode": "markers", 
  "name": "Peace", 
  "text": ["Malala Yousafzai<br>2014", "Ellen Johnson Sirleaf<br>2011", "Leymah Gbowee<br>2011", "Tawakkol Karman<br>2011", "Wangari Muta Maathai<br>2004", "Shirin Ebadi<br>2003", "Jody Williams<br>1997", "Rigoberta Menchú Tum<br>1992", "Aung San Suu Kyi <br>1991", "Alva Myrdal<br>1982", "Mother Teresa <br>1979", "Betty Williams<br>1976", "Mairead Corrigan<br>1976", "Emily Greene Balch<br>1946", "Jane Addams<br>1931", "Bertha von Suttner<br>1905"], 
  "type": "scatter"
}
trace2 = {
  "x": [-11.3463673317, -11.0131500283, -13.264699081, -12.200293625, -8.12135473427, -9.78427315866, -13.9811187779, -8.55255356814, -6.85881395361, -7.43620299457, -8.49104530233, -10.6550689494, -6.95865228066, -8.5], 
  "y": [-10.2673504021, -12.3394591817, -10.6440496107, -12.4076113444, -13.1755651981, -11.3545735549, -9.69992815669, -11.5184531998, -10.1341009226, -6.33093777656, -9.75176607215, -7.18130264912, -11.474639929, -8], 
  "hoverinfo": "text", 
  "marker": {
    "color": "#f28dce", 
    "line": {
      "color": "#000000", 
      "width": 0.5
    }, 
    "size": 20, 
    "symbol": "dot"
  }, 
  "mode": "markers", 
  "name": "Literature", 
  "text": ["Svetlana Alexievich<br>2015", "Alice Munro<br>2013", "Herta Müller<br>2009", "Doris Lessing<br>2007", "Elfriede Jelinek<br>2004", "Wislawa Szymborska<br>1996", "Toni Morrison<br>1993", "Nadine Gordimer<br>1991", "Nelly Sachs<br>1966", "Gabriela Mistral<br>1945", "Pearl Buck<br>1938", "Sigrid Undset<br>1928", "Grazia Deledda<br>1926", "Selma O.L. Lagerlof<br>1909"], 
  "type": "scatter"
}
trace3 = {
  "x": [3.15292526224, 8.07178175014, 6.15659185994, 4.08975544205, 6.78546647902, 7.65472350126, 2.13652765648, 2.01332485489, 5.26069706077, 5.40401872045, 7.35129175604, 4.38427329817], 
  "y": [-9.55158980762, -10.8402225804, -10.1341818399, -12.2402763093, -8.18078681213, -13.7384953693, -13.4273965264, -10.1140496913, -8.73154011068, -13.0963959246, -12.0772577897, -11.3478049636], 
  "hoverinfo": "text", 
  "marker": {
    "color": "#7c8efb", 
    "line": {
      "color": "#000000", 
      "width": 0.5
    }, 
    "size": 20, 
    "symbol": "dot"
  }, 
  "mode": "markers", 
  "name": "Medicine", 
  "text": ["Youyou Tu<br>2015", "May-Britt Moser<br>2014", "Elizabeth H. Blackburn<br>2009", "Carol W. Greider<br>2009", "Françoise Barré-Sinoussi<br>2008", "Linda B. Buck<br>2004", "Christiane Nüsslein-Volhard<br>1995", "Gertrude B. Elion<br>1988", "Rita Levi-Montalcini<br>1986", "Barbara McClintock<br>1983", "Rosalyn Yalow<br>1977", "Gerty Theresa Cori<br>1947"], 
  "type": "scatter"
}
trace4 = {
  "x": [-10.6668291602, -8.62897659658, -7.59668318057, -9.05457026619], 
  "y": [-2.13343530587, -1.48148357831, -0.237285562438, -0.259210076401], 
  "hoverinfo": "text", 
  "marker": {
    "color": "#fcb19b", 
    "line": {
      "color": "#FFFFFF", 
      "width": 0.5
    }, 
    "size": 20, 
    "symbol": "dot"
  }, 
  "mode": "markers", 
  "name": "Chemistry", 
  "text": ["Ada E. Yonath<br>2009", "Dorothy Crowfoot Hodgkin<br>1964", "Irène Joliot-Curie<br>1935", "Marie Curie<br>1911"], 
  "type": "scatter"
}
trace5 = {
  "x": [9.8, 8], 
  "y": [3.2, 4], 
  "hoverinfo": "text", 
  "marker": {
    "color": "#fefe9a", 
    "line": {
      "color": "#000000", 
      "width": 0.5
    }, 
    "size": 20, 
    "symbol": "dot"
  }, 
  "mode": "markers", 
  "name": "Physics", 
  "opacity": 0.9, 
  "text": ["Maria Goeppert Mayer<br>1963", "Marie Curie<br>1903"], 
  "type": "scatter"
}
trace6 = {
  "x": [-3], 
  "y": [-7], 
  "hoverinfo": "text", 
  "marker": {
    "color": "rgb(180,42,107)", 
    "line": {
      "color": "#FFFFFF", 
      "width": 0.5
    }, 
    "size": 20, 
    "symbol": "dot"
  }, 
  "mode": "markers", 
  "name": "Economy", 
  "opacity": 0.75, 
  "text": "Elinor Ostrom<br>2009", 
  "type": "scatter"
}
data = Data([trace1, trace2, trace3, trace4, trace5, trace6])
layout = {
  "annotations": [
    {
      "x": 0, 
      "y": -0.14, 
      "font": {"size": 0}, 
      "showarrow": False, 
      "text": "Data source: <a href='http://www.nobelprize.org/nobel_prizes/lists/women.html'>[1]</a>", 
      "xanchor": "left", 
      "xref": "paper", 
      "yanchor": "bottom", 
      "yref": "paper"
    }
  ], 
  "height": 525, 
  "hovermode": "closest", 
  "margin": {
    "r": 200, 
    "t": 100, 
    "b": 80, 
    "l": 80
  }, 
  "plot_bgcolor": "rgb(50,50,50)", 
  "title": "Nobel Prize Awarded Women", 
  "width": 650, 
  "xaxis": {
    "mirror": True, 
    "showgrid": False, 
    "showline": True, 
    "showticklabels": False, 
    "ticks": "", 
    "zeroline": False
  }, 
  "yaxis": {
    "mirror": True, 
    "showgrid": False, 
    "showline": True, 
    "showticklabels": False, 
    "ticks": "", 
    "zeroline": False
  }
}
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)
