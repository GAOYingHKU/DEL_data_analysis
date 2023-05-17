import matplotlib.pyplot as plt
import argparse


plt.rcParams['font.sans-serif'] = ['Arial']

etoga = argparse.ArgumentParser(description='if the generated figure from the main script is too large or contains too many points, you could use this script to zoom in your figure: example: python ef_plot_2D_zoom_in.py -i /Users/jy/Desktop/ZY/1stm1h7uLVG/ef/test-3_2.txt -xlim 10 -ylim 10 -xaxis 2 -yaxis 4 -xlabel "count" -ylabel "enrichment fold" -o /Users/jy/Desktop/ZY/1stm1h7uLVG/ef_plot/test-3_2.png')
etoga.add_argument('-i', type=str, nargs=1, required=True, help='the input file, please add the full path')
etoga.add_argument('-xlim',type=float,nargs=1, required=True, help='the maximum x scale that will be displayed')
etoga.add_argument('-ylim',type=float,nargs=1, required=True, help='the maximum y scale that will be displayed')
etoga.add_argument('-xaxis',type=int,nargs=1, required=True, help='the column selected as x-axis, start from 0')
etoga.add_argument('-yaxis',type=int,nargs=1, required=True, help='the column selected as y-axis, start from 0')
etoga.add_argument('-xlabel',type=str,nargs=1, required=True, help='the title of x-axis')
etoga.add_argument('-ylabel',type=str,nargs=1, required=True, help='the title of y-axis')
etoga.add_argument('-o', type=str, nargs=1, required=True, help='the output file, please add the full path')

args = etoga.parse_args()

def ef_plot(i,xlim,ylim,xaxis,yaxis,xlabel,ylabel,o):
    #indir='/Users/jy/Desktop/ZY/1stm1h7uLVG/ef/'
    #outdir='/Users/jy/Desktop/ZY/1stm1h7uLVG/ef_plot/'
    x=[float(line.split()[xaxis]) for line in open(i,'r')]
    y=[float(line.split()[yaxis]) for line in open(i,'r')]
    plt.scatter(x, y, alpha=0.6)
    plt.xlabel(xlabel)
    plt.xlim(0,xlim)
    plt.ylim(0,ylim)
    plt.ylabel(ylabel)
    plt.savefig(o)



ef_plot(args.i[0],args.xlim[0],args.ylim[0],args.xaxis[0],args.yaxis[0],args.xlabel[0],args.ylabel[0],args.o[0])




