import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

src = os.path.join('data','dic_p17_labeled.tsv')

df = pd.read_table(
		src,
        names = ['old',
                 'new',
                 'count',
                 'chars_nb',
                 'old_chars',
                 'new_chars',
                 'rules'])

rules = {}
i = 0
totalCount = 0

for line in df["rules"]:
   '''if len(line)>1:
      print(line)
      print(df["count"][i])
   '''
   if line=="[]":
      line = "règle inconnue"
   if line in rules.keys():
      rules[line] += df["count"][i]
   else:
      rules[line] = df["count"][i]
   totalCount += df["count"][i]
   i += 1

# order rules according to decreasing frequency
rules = dict(sorted(rules.items(), key=lambda item: -item[1]))
print(totalCount)

# histogram
x = list(rules.keys())
y = list(rules.values())
fig = px.bar(x=x, y=y, labels={'x':'label', 'y':'number of maximal distinct subword labels over '+str(totalCount)})

'''go.Figure()
fig.add_trace(go.Histogram(histfunc="sum", y=y, x=x, name="sum"))
'''
'''

# pie chart
fig = px.pie(
		df,
		values = 'count',
		names = 'labels',
		title = 'Modernization Observation Labels')
'''
# show
fig.show()

# save
fig.write_html(os.path.join('data','rules_chart.html'))