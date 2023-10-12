import dash
#import dash_core_components as dcc
#import dash_html_components as html
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sys
import numpy as np
import argparse



working_path = str(os.getcwd())


etoga = argparse.ArgumentParser(description='')
etoga.add_argument('-fn', type=str, nargs=1, required=True, help='')
etoga.add_argument('-count_threshold',type=int,nargs=1, required=True, help='')
etoga.add_argument('-ef_threshold',type=float,nargs=1, required=True, help='')
etoga.add_argument('-path',type=str,nargs=1, required=True, help='')


args = etoga.parse_args()


data={'x':[],'y':[],'z':[],'count':[],'ef':[]}
for line in open(args.path[0]+os.sep+args.fn[0],'r'):
    if int(line.split('\t')[2])<args.count_threshold[0] or float(line.split('\t')[-1])<args.ef_threshold[0]:continue
    data['x'].append(int(line.split('\t')[0].split('-')[0]))
    data['y'].append(int(line.split('\t')[0].split('-')[1]))
    data['z'].append(int(line.split('\t')[0].split('-')[2]))
    data['count'].append(int(line.split('\t')[2]))
    data['ef'].append(float(line.split('\t')[-1]))
df=pd.DataFrame(data)


fig = px.scatter_3d(df,x='x', y='y', z='z',color="count", size='ef',size_max=40,template="plotly", color_continuous_scale=px.colors.sequential.Turbo)


# tight layout
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),title_font_family='Arial Black',title_font_size=10,legend_font_family='Arial Black',legend_font_size=6,legend_title_font_family='Arial Black',legend_title_font_size=8,font_family='Arial Black')
fig.write_html('%s_%s_%s_3D.html'%(args.fn[0].split('.')[0],str(args.count_threshold[0]),str(args.ef_threshold[0])))

