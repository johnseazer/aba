import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

src = 'data/dic_p17_labeled.tsv'

df = pd.read_table(
		src,
        names = ['old',
                 'new',
                 'count',
                 'chars_nb',
                 'old_chars',
                 'new_chars',
                 'rules'])

'''
# histogram
x = df['rules']
y = df['count']
fig = go.Figure()
fig.add_trace(go.Histogram(histfunc="sum", y=y, x=x, name="sum"))
'''

# pie chart
fig = px.pie(
		df,
		values = 'count',
		names = 'rules',
		title = 'Modernization Rules')

# show
fig.show()

# save
fig.write_html('data/rules_chart.html')