#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Clear all

from IPython import get_ipython
get_ipython().magic('reset -sf')

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as scipy
import seaborn as sns


# Set working directories and seed

outputpath = '/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework4/output'

data = pd.read_csv('/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework4/fishbycatch.txt',sep=",")
fish = pd.wide_to_long(data, stubnames=['bycatch','salmon','shrimp'],i='firm', j="month")
fish = fish.reset_index(level=['firm', 'month'])  ## I need to pull out month....

###Q1 
trend=fish.groupby(['treated','month'])['bycatch'].mean()
trend = trend.reset_index(level=['treated', 'month']) 
trend_fig = sns.lineplot(data=trend, x="month", y="bycatch", hue="treated")
plt.savefig("par_trend.png")

##Q2 
#four categories
fish_pre_treat=fish[(fish["month"]<13) & (fish["treated"]==1)]
fish_post_treat=fish[(fish["month"]>12) & (fish["treated"]==1)]
fish_pre_control=fish[(fish["month"]<13) & (fish["treated"]==0)]
fish_post_control=fish[(fish["month"]>12) & (fish["treated"]==0)]

DID=(fish_post_treat['bycatch'].mean()-fish_pre_treat['bycatch'].mean())-(fish_post_control['bycatch'].mean()-fish_pre_control['bycatch'].mean())
DID=np.round(DID,2)

##Q3 
nobs = fish.count().max() #max() is necessary to get just one number 

#making treat_it
fish['tr']=np.empty([nobs, 1]) 
for r in range(nobs):
    if fish["treated"][r]==0 : fish['tr'][r]=0
    elif (fish["month"][r]>=13) & (fish["treated"][r]==1): fish['tr'][r]=1
    else: fish['tr'][r]=0
    
#a
#subset including Dec 2017 and Jan 2018
fish2=fish[(fish["month"]==12)|(fish["month"]==13)]
nobs2=fish2.count().max()

#making lamda_2017
#one of my friend taught me numpy where.. what a revolution
fish2['t_2017']=np.where((fish2["month"]==12) , 1, 0) 

xvar1=pd.concat([fish2['t_2017'],fish2['treated'],fish2['tr']], axis=1)
xvar1=sm.add_constant(xvar1,prepend=True)

yvar1=fish2['bycatch']    
ols1=sm.OLS(yvar1,xvar1).fit()
olscoef1=ols1.params
#how can we extract standard error from OLS result???
olsse1=olscoef1/ols1.tvalues

olscoef1=np.array([olscoef1['treated'], olscoef1['tr']])
olscoef1=np.round(olscoef1,2)
olsse1=np.array([olsse1['treated'], olsse1['tr']])
olsse1=np.round(olsse1,2)

ols_result1 = pd.concat([pd.Series(olscoef1), pd.Series(olsse1)],axis = 1).stack()
              
#b
time = pd.get_dummies(fish['month'],prefix = 'time',drop_first = True) #time dummy
firm_dum = pd.get_dummies(fish['firm'],prefix = 'firm',drop_first = True)
xvar2=pd.concat([firm_dum,time,fish['treated'],fish['tr']], axis=1)
yvar2=fish['bycatch']    

ols2=sm.OLS(yvar2,xvar2).fit(cov_type = 'cluster', cov_kwds={"groups":fish['firm']})
olscoef2=ols2.params
olsse2=olscoef2/ols2.tvalues
olscoef2=np.array([olscoef2['treated'], olscoef2['tr']])
olscoef2=np.round(olscoef2,2)
olsse2=np.array([olsse2['treated'], olsse2['tr']])
olsse2=np.round(olsse2,2)

ols_result2 = pd.concat([pd.Series(olscoef2), pd.Series(olsse2)],axis = 1).stack()


#c
xvar3=pd.concat([xvar2, fish['firmsize'], fish['salmon'], fish['shrimp']], axis=1)
yvar3=fish['bycatch']    
ols3=sm.OLS(yvar3,xvar3).fit(cov_type = 'cluster', cov_kwds={"groups":fish['firm']})
olscoef3=ols3.params
olsse3=olscoef3/ols3.tvalues

olscoef3=np.array([olscoef3['treated'], olscoef3['tr'],olscoef3['firmsize'],olscoef3['salmon'],olscoef3['shrimp']])
np.set_printoptions(suppress=True)
olscoef3=np.round(olscoef3,2)
olsse3=np.array([olsse3['treated'], olsse3['tr'],olsse3['firmsize'],olsse3['salmon'],olsse3['shrimp']])
olsse3=np.round(olsse3,2)

ols_result3 = pd.concat([pd.Series(olscoef3), pd.Series(olsse3)],axis = 1).stack()

result=pd.concat([ols_result1,ols_result2, ols_result3], axis=1)
result = result.replace(np.nan, '')
colnames = ['(a)','(b)','(c)']
result.columns=colnames


#adding observation
obs=pd.DataFrame({"(a)":[nobs2],
                    "(b)":[nobs],
                    "(c)":[nobs]})

result=result.append(obs)

rownames =pd.concat([pd.Series(['treated group','treatment','firmsize','salmon','shrimp','Observation']),pd.Series([' ',' ',' ',' ',' '])],axis = 1).stack()
result.index=rownames

#How can I add () for standard errors?

result.to_latex('result_python.tex') 








