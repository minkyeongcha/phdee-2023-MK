#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample code to get you started -- Dylan Brewer

# Clear all

from IPython import get_ipython
get_ipython().magic('reset -sf')

# Import packages - you may need to type "conda install numpy" the first time you use a package, for example.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import scipy.stats as scipy

# Set working directories and seed

outputpath = '/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework2/output'
# Normally I will also have a datapath where I store the original data if I am working on a small enough csv file.

data = pd.read_csv('/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework2/kwh.csv')

##I wish I could find simpler, canned routine for this.. but I couldn't, so computed these separately
### Generate means
mean_control = data[data['retrofit']==0].mean().drop('retrofit')
mean_treat = data[data['retrofit']==1].mean().drop('retrofit')

## Generate standard deviations
stdev_control = data[data['retrofit']==0].std().drop('retrofit')
stdev_treat = data[data['retrofit']==1].std().drop('retrofit')

## Get number of observations
nobs_control = data[data['retrofit']==0].count().min()
nobs_treat= data[data['retrofit']==1].count().min()

## Set the row and column names - from hw1
rownames = pd.concat([pd.Series(['electricity','sqft','temp', 'Observations']),pd.Series([' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
colnames = [('Control','(s.d)'),('Treatment','(s.d)'),('difference-in-means','(p-value)')]

## Format means and std devs to display to two decimal places
mean_control = mean_control.map('{:.2f}'.format)
mean_treat = mean_treat.map('{:.2f}'.format)
stdev_control = stdev_control.map('({:.2f})'.format)
stdev_treat = stdev_treat.map('({:.2f})'.format)

col_control = pd.concat([mean_control,stdev_control, pd.Series(nobs_control)], axis = 1).stack()

col_treat = pd.concat([mean_treat,stdev_treat, pd.Series(nobs_treat)], axis = 1).stack()

col_control = pd.DataFrame(col_control)
col_control.index = rownames

col_treat = pd.DataFrame(col_treat)
col_treat.index = rownames

####now working on difference-in-mean tests
result, pvalue=scipy.ttest_ind(data[data['retrofit']==1].drop('retrofit',1), data[data['retrofit']==0].drop('retrofit',1), equal_var = False)
result = pd.Series(result,['electricity', 'sqft', 'temp'])
pvalue = pd.Series(pvalue,['electricity', 'sqft', 'temp'])

result = result.map('{:.2f}'.format)
pvalue = pvalue.map('({:.2f})'.format)
col_diff=pd.concat([result,pvalue, pd.Series([''])], axis = 1).stack()

col_diff = pd.DataFrame(col_diff)
col_diff.index = rownames

#and combining all!
table1 = pd.concat([col_control,col_treat,col_diff], axis = 1)
table1.columns = pd.MultiIndex.from_tuples(colnames)
table1.index = rownames

os.chdir(outputpath) # Output directly to LaTeX folder

table1.to_latex('table1_python.tex') 

###kernel density plot
kde=sns.kdeplot(data=data, x='electricity',hue='retrofit')
kde_fig=kde.get_figure()
kde_fig.savefig('kernel plot.pdf',format='pdf') 
plt.show()

##OLS
##1) OLS by hand
yvar=data['electricity'].to_numpy()
xvar=data.drop('electricity', axis=1).to_numpy()
nobs = np.array(nobs_control+nobs_treat)
a0 = np.ones( (nobs,1) )
xvar=np.concatenate((xvar,a0 ), axis=1)

ols_a = np.matmul(np.linalg.inv((np.matmul(xvar.T, xvar))), np.matmul(xvar.T, yvar))
ols_a=np.around(ols_a, decimals=2)

##2) by simulated least squares
from scipy.optimize import minimize

def obj(beta, yvar, xvar):return np.sum((yvar-np.matmul(xvar,beta))**2)
beta0=np.array([1,1,1,1]).T  #initial beta to begin simulation
ols_b=minimize(obj,beta0, args=(yvar, xvar)).x
ols_b=np.around(ols_b, decimals=2)

##c) by canned routine
ols = sm.OLS(data['electricity'],xvar).fit()
ols_c = ols.params.to_numpy()
ols_c=np.around(ols_c, decimals=2)

##combining!
rownames =pd.Series(['sqft','retrofit','temp','Constant','Observations'])
colnames = pd.Series(['by hand (a)','simulated LS (b)', 'Package (c)'])
table2 = pd.DataFrame((np.append(ols_a,nobs),np.append(ols_b,pd.Series('')),np.append(ols_c,pd.Series('')))).T
table2.index = rownames
table2.columns = colnames

table2.to_latex('table2_python.tex') 
