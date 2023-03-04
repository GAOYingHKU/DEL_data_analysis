import argparse
import pandas as pd
import os
import sys
import numpy as np
import itertools
import matplotlib.pyplot as plt
#import dash
#from dash import html
#from dash import dcc
#from dash.dependencies import Input, Output
#import plotly.express as px
from Bio import SeqIO
import time
from collections import Counter

start=time.time()
working_path = str(os.getcwd())
plt.rcParams['font.sans-serif'] = ['Arial']

etoga = argparse.ArgumentParser(description='This python script is used to calculate the enrichment fold of samples compared to control, including three steps. step1: identify the sequences of interest from the library and calculate the normalized counts (divide the total number of counts); step2: based on the control list, calculate the enrichment fold of samples; step3: plot the figures of enrichment fold, x-axis is "sequence count", y-axis is "enrichment fold", if ypou want to adjust the figures generated in step3, we also provide additional python scripts to help you beautify the figures.')
etoga.add_argument('-path', type=str, nargs=1, required=True, help='the folder of input fastq file, with suffix "fq,fastq"')
etoga.add_argument('-codelist',type=str,nargs=1, required=True, help='provide an excel with sequences coding chemicals of each building block, with suffix "xlsx"')
etoga.add_argument('-BBs_num',type=int,nargs=1, required=True, help='numbers of building blocks, provide in the codelist file')
etoga.add_argument('-sequence_structure',type=str,nargs=1, required=True, help='region of code for each building block, corresponding to codelist file')
etoga.add_argument('-add_common_site',type=str,nargs=1, default=['off'],help='if you want to define the whole sequences to 100 %% match the expected, you should add common site sequences and region of site in the sequence sequence_structure file')
etoga.add_argument('-control',type=str,nargs=1,required=True, help='provide control names for each sample in the control.xlsx file: in this project, control is selection without target; in traditional DEL, control is Pre-selection')
etoga.add_argument('-skip_count',type=str,nargs=1, default=['off'],help='if you have successfully finished step1 and want to rerun the step2 and step3, please set "on" to reduce computational time. ')
etoga.add_argument('-skip_ef',type=str,nargs=1, default=['off'],help='if you have successfully finished step1 and step2 and want to rerun step3, please set both -skip_count and -skip_ef "on" to reduce computational time. ')
etoga.add_argument('-o', type=str, nargs=1, required=True, help='the folder of output file')

args = etoga.parse_args()



def iter_code(df,codenum,add,ann,output):
    label=[]
    seq=[]
    keylist=list(df.keys())
    for i in range(codenum):
        label.append(list(df[keylist[i]].dropna()))
    if add=='off':       
       for i in range(codenum,codenum*2):
           seq.append(list(df[keylist[i]].dropna()))
    if add=='on':
       for line in ann:
            if 'common' in line:
                seq.append([line.split(',')[1]])
            else:
                seq.append(list(df[line.split(',')[0]].dropna()))
    _label=['-'.join(j) for j in itertools.product(*label)]
    _seq=[''.join(j) for j in itertools.product(*seq)]
    fo=open(working_path+os.sep+'config/generated_code.txt','w')
    for _i,_j in zip(_label,_seq):
        fo.write('%s\t%s\n'%(_i,_j))
    fo.close()
    return _label,_seq



def fastq_process(path,fn,ann):
    _dict={}
    fa=SeqIO.parse(path+os.sep+fn,'fastq')
    for r in fa:
        fullseq=r.seq
        tmpseq=''
        for line in ann:
            tmpseq+=fullseq[int(line.split(',')[-2])-1:int(line.split(',')[-1])]
        if tmpseq in _dict:
            _dict[tmpseq]+=1
        else:
            _dict[tmpseq]=1
    return _dict




def code_combination_count(code,codenum,coderegion,path,add,output):
    os.system('mkdir -p %s/%s/percent'%(working_path,output))
    df=pd.read_excel(working_path+os.sep+'config/'+code)
    ann=[]
    with open(working_path+os.sep+'config/'+coderegion,'r') as fi:
         for line in fi:
             if add=='off':
                if 'common' in line:continue
                ann.append(line.strip('\n'))
             else:
                ann.append(line.strip('\n'))
    label,seq=iter_code(df,codenum,add,ann,output)
    count={}
    usenum={}
    for fn in os.listdir(working_path+os.sep+path):
        if fn.startswith("."):continue
        if os.path.splitext(fn)[-1] not in ['.fq','.fastq']:continue
        print('read %s...'%fn)
        _dict=fastq_process(path,fn,ann)
        _fn=fn.split('.')[0]
        count=[]
        usenum[_fn]=0
        for i in seq:
            if i in _dict:
               usenum[_fn]+=_dict[i]
               count.append(_dict[i])
            else:
               count.append(0.01314)
        fo=open('%s/%s/percent/%s.txt'%(working_path,output,_fn),'w')
        for j,k in zip(seq,count):
            fo.write('%s\t%.5f\t%.15f\n'%(j,k,k/usenum[_fn]))
        fo.close()
    



def read_percent(fn,output):
    indir='%s/%s/percent/'%(working_path,output)
    tmp={}
    with open(indir+'%s.txt'%fn,'r') as fi:
         for line in fi:
             tmp[line.split('\t')[0]]=[float(line.split('\t')[1]),float(line.strip('\n').split('\t')[-1])]
    return tmp



def cal_percent_ef(control,output):
    os.system('mkdir -p %s/%s/ef'%(working_path,output))
    df=pd.read_excel(working_path+os.sep+'config/'+control)
    controllist,sample=np.array(df['control'].dropna()),np.array(df['sample'].dropna())
    for c,s in zip(controllist,sample):
        ct=read_percent(c,output)
        sam=read_percent(s,output)
        fo=open(working_path+os.sep+output+os.sep+'ef/%s_%s.txt'%(s,c),'w')
        for i in ct:
            fo.write('%s\t%d\t%f\t%d\t%f\t%f\n'%(i,ct[i][0],ct[i][1],sam[i][0],sam[i][1],sam[i][1]/ct[i][1]))
        fo.close()


def ef_plot_2D(output):
    os.system('mkdir -p %s/%s/ef_plot'%(working_path,output))
    for fn in os.listdir(working_path+os.sep+output+os.sep+'ef'):
        x=[]
        y=[]
        with open(working_path+os.sep+output+os.sep+'ef/'+fn,'r') as fi:
             for line in fi:
                 a=int(line.split('\t')[3])
                 b=float(line.strip('\n').split('\t')[-1])
                 x.append(a)
                 y.append(b)
        plt.scatter(x, y, alpha=0.6)
        plt.xlabel('sequence count',fontweight='bold',fontsize=12)
        plt.xticks(fontproperties='Arial',weight='bold')
        plt.yticks(fontproperties='Arial',weight='bold')   
        plt.ylabel('enrichment fold',fontweight='bold',fontsize=12)
        plt.savefig(working_path+os.sep+output+'/ef_plot/'+fn.replace('.txt','.png'))
        plt.close()





if args.skip_count[0]=='off':
   code_combination_count(args.codelist[0],args.BBs_num[0],args.sequence_structure[0],args.path[0],args.add_common_site[0],args.o[0])
if args.skip_ef[0]=='off':
   cal_percent_ef(args.control[0],args.o[0])
ef_plot_2D(args.o[0])



end=time.time()
print('time:',end-start)







    












