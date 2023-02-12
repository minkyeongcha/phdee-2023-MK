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
from scipy.stats import bootstrap


# Set working directories and seed

outputpath = '/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework3/output'

data = pd.read_csv('/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework2/kwh.csv')

###Q1
##(e) getting the values 
yvar=np.log(data['electricity'])
xvar=pd.concat([data['retrofit'], np.log(data['temp'])],axis=1)
xvar=pd.concat([xvar, np.log(data['sqft'])],axis=1)
xvar=sm.add_constant(xvar,prepend=False)

nobs = data.count().max() #max() is necessary to get just one number 
reps = 1000 # number of bootstrap replications
params = len(xvar.columns) #number of parameters

ols=sm.OLS(yvar,xvar).fit()
olscoef=ols.params.to_numpy()

par_retrofit = ols.params['retrofit']
par_sqft = ols.params['sqft']
par_temp = ols.params['temp']

def margin_d1(par_retrofit, yvar, xvar): return(((np.exp(par_retrofit)-1)*yvar)/np.exp(par_retrofit)**(xvar['retrofit']))
def margin_z1(par_sqft, yvar, xvar): return(par_sqft*yvar/(xvar['sqft']))
def margin_z2(par_temp, yvar, xvar): return(par_temp*yvar/(xvar['temp']))

marginlist=np.empty([nobs, params-1])
marginlist[:,0]=margin_d1(par_retrofit, yvar, xvar)
marginlist[:,1]=margin_z1(par_sqft, yvar, xvar)
marginlist[:,2]=margin_z2(par_temp, yvar, xvar)
marginlist = np.round(marginlist,2).mean(axis=0)

##bootstrap marginal effect - referring to the sample code in homework 1
##setting
np.random.seed(123456)

bidx = np.random.choice(nobs,(nobs,reps)) # Generates random numbers on the interval [0,nobs3] and produces a nobs3 x breps sized array

#empty arrays that we can record bootstrap results
olslist = np.empty((reps,params))
margin=np.empty((reps,params-1))
margin2=np.empty((reps,params-1))

data2=pd.concat([yvar,xvar], axis=1)
#data2=pd.DataFrame(data2,columns = ['electricity','retrofit','temp','sqft','constant'])

## Sample with replacement to get the size of the sample on each iteration
for r in range(reps):
    datab = data2.iloc[bidx[:,r]]
    
    yvar2=datab['electricity']
    xvar2=datab.drop('electricity',1)
    
    ols2=sm.OLS(yvar2,xvar2).fit()
    par_retrofit2 = ols2.params['retrofit']
    par_sqft2 = ols2.params['sqft']
    par_temp2 = ols2.params['temp']
    
    olslist[r,:] = ols2.params.to_numpy()
    margin[:,0]=margin_d1(par_retrofit2, yvar2, xvar2)
    margin[:,1]=margin_z1(par_sqft2, yvar2, xvar2)
    margin[:,2]=margin_z2(par_temp2, yvar2, xvar2)
    margin2 = np.mean(margin,axis = 0)  #just to compare mean estimates 
    
## Extract 2.5th and 97.5th percentile
lb_ols = np.percentile(olslist,2.5,axis = 0,interpolation = 'lower')
ub_ols = np.percentile(olslist,97.5,axis = 0,interpolation = 'higher')

lb_margin = np.percentile(margin,2.5,axis = 0,interpolation = 'lower')
ub_margin = np.percentile(margin,97.5,axis = 0,interpolation = 'higher')

lb_ols = pd.Series(np.round(lb_ols,2)) 
ub_ols = pd.Series(np.round(ub_ols,2))
lb_margin = pd.Series(np.round(lb_margin,2)) 
ub_margin = pd.Series(np.round(ub_margin,2))

ci_ols = '(' + lb_ols.map(str) + ', ' + ub_ols.map(str) + ')'
ci_margin = '(' + lb_margin.map(str) + ', ' + ub_margin.map(str) + ')'

##combining!
olscoef=np.round(olscoef,2)
marginlist=np.round(marginlist,2)
olslist2=pd.DataFrame(olscoef)
marginlist2=pd.DataFrame(marginlist)

#I have different marginal effect estimates, so I am reporting both
margin2=np.round(margin2, 2)
marginlist3=pd.DataFrame(margin2)

#making room for constant
marginlist2=marginlist2.append(pd.Series(['']), ignore_index=True)
ci_margin=ci_margin.append(pd.Series(['']), ignore_index=True)
marginlist3=marginlist3.append(pd.Series(['']), ignore_index=True)

rownames =pd.concat([pd.Series(['retrofit','ln(temp)','ln(sqft)','alpha','Observations']),pd.Series([' ',' ',' ',' ',])],axis = 1).stack()
colnames = pd.Series(['Regression estimates','Margin effect(1)', 'Margin effect(2)'])

col_ols=pd.concat([olslist2,ci_ols], axis = 1).stack()
col_ols=col_ols.append(pd.Series(nobs))

col_margin=pd.concat([marginlist2,ci_margin], axis = 1).stack()
col_margin=col_margin.append(pd.Series(nobs))

col_margin2=pd.concat([marginlist3,ci_margin], axis = 1).stack()
col_margin2=col_margin2.append(pd.Series(nobs))

#why is table1 = pd.DataFrame(col_ols, col_margin) not working??
table1 = pd.concat([col_ols, col_margin, col_margin2], axis=1)
table1.index = rownames
table1.columns = colnames

table1.to_latex('table1.tex') 

#plot....(f) referring to https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.07-Error-Bars/
yer1 = [ub_margin[2]-margin2[2]]
yer2 = [ub_margin[1]-margin2[1]]

labels = ['temp', 'sqft']
x_pos = np.arange(len(labels))
mean = [margin2[2], margin2[1]]
error = [yer1, yer2]


fig, ax = plt.subplots()
ax.bar(x_pos, mean,
       yerr=error,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)
ax.set_ylabel('Average Marginal Effect')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels)
ax.set_title('')
ax.yaxis.grid(True)

plt.tight_layout()
plt.savefig('Average Marginal Effect')
plt.show()








