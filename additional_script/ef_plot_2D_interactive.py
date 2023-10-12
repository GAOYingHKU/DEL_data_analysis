import pandas as pd
import numpy as np
import sys
from bokeh.io import show, curdoc,output_file
from bokeh.plotting import figure

from bokeh.models import  HoverTool, ColumnDataSource
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
    data['x'].append(str(line.split('\t')[0].split('-')[0]))
    data['y'].append(str(line.split('\t')[0].split('-')[1]))
    data['z'].append(str(line.split('\t')[0].split('-')[2]))
    data['count'].append(int(line.split()[2]))
    data['ef'].append(float(line.split()[-1]))


output_file('%s_%s_%s_2D.html'%(ipt,str(args.count_threshold[0]),str(args.ef_threshold[0])))


src = ColumnDataSource(data)

p = figure(plot_width = 700, plot_height = 700,
              title = 'count vs enrichment fold',
              x_axis_label = 'count', y_axis_label = 'enrichment fold')
p.circle(source=src,x='count',y='ef',size=8,color='blue',alpha=0.5,legend_label='point')
hover = HoverTool(tooltips=[('x','@x'),('y','@y'),('z','@z'),('count', '@count'),('enrichment fold','@ef')], mode='mouse')


def style(p):
    # Title
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.title.text_font = 'serif'

    # Axis titles
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_style = 'bold'

    # Tick labels
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'

    return p

p = style(p)
p.add_tools(hover)
show(p)
