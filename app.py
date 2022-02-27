import pandas as pd
import numpy as np
import plotly.express as px
from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_html_components as html
app=JupyterDash(__name__)
server=app.server
df = pd.read_csv('https://raw.githubusercontent.com/srinathkr07/IPL-Data-Analysis/master/matches.csv')
df=df.drop(columns='id')
df=df.fillna(0)
mappings={'Rising Pune Supergiant':'Rising Pune Supergiants','Delhi Capitals':'Delhi Daredevils'}
df['team1']=df['team1'].replace(mappings)
df['team2']=df['team2'].replace(mappings)
df['winner']=df['winner'].replace(mappings)
df['toss_winner']=df['toss_winner'].replace(mappings)
loser=[]
for i in range(756):
  if (df.iloc[i,3])!=(df.iloc[i,9]):
    loser.append(df.iloc[i,3])
  elif (df.iloc[i,9])==0:
    loser.append(0)
  else:
    loser.append(df.iloc[i,4])
df['Loser']=loser
total={}
count=0
for i in df['team1'].unique():
  for m in range(756):
    if i==df.iloc[m,3]:
      count+=1
    else:
      if i==df.iloc[m,4]:
        count+=1
  total[i]=count
  count=0
  match=[]
for i in df['winner']:
  for j,k in total.items():
    if i==j:
      match.append(k)
    elif i==0:
      match.append(0)
      break
df['Total_matches_played_by_winner']=match
pie=px.pie(data_frame=df,names='winner',title='Best team based on Number of Wins',hole=0.2,hover_data=['Total_matches_played_by_winner'])
pie.update_traces(textinfo="label+value",textposition='inside')
bar=px.bar(df,x='player_of_match',color='player_of_match',title='Best Player based on Player of the Match')
scat=px.scatter_3d(df,x='winner',y='Loser',z='win_by_runs',color='win_by_runs',size='win_by_runs',title='Best team based on Win by Runs')
dfh=df.query("win_by_wickets>0")
sun1= px.sunburst(dfh, path=['winner', 'win_by_wickets'],title='Best Team based on Win by Wickets')
sun1.update_layout(margin = dict(t=25, l=25, r=25, b=25))
sun1.update_traces(textinfo="label+value",maxdepth=1)
fig=px.bar(df,x='venue',color='winner',title='Luckiest Venue for Each Team',animation_frame='winner',barmode='relative')
fig.update_layout(margin=dict(l=100, r=20, t=100, b=200),paper_bgcolor="beige",title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 150)
fig['layout']['sliders'][0]['pad']=dict(r= 20, t= 200,)
sun= px.sunburst(df, path=['toss_winner', 'winner'],title='Winning probability by Winning Toss')
sun.update_layout(margin = dict(t=25, l=25, r=25, b=25))
sun.update_traces(textinfo="label+percent parent+value")
app.layout=html.Div( children=[dcc.Graph(
       id='example-graph-1',
       figure=pie
   ),dcc.Graph(
       id='example-graph2',
       figure=bar
   ),dcc.Graph(
       id='example-graph3',
       figure=scat
   ),dcc.Graph(
       id='example-graph4',
       figure=sun1
   ),dcc.Graph(
       id='example-graph5',
       figure=fig
   ),dcc.Graph(
       id='example-graph6',
       figure=sun
   )
])
 
if __name__ == '__main__':
   app.run_server(debug=True)
