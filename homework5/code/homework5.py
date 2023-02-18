#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Clear all

from IPython import get_ipython
get_ipython().magic('reset -sf')

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IVGMM


# Set working directories and seed

outputpath = '/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework5/output'
data=pd.read_csv('/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework5/instrumentalvehicles.csv')

###Q1 
xvar=pd.concat([data['mpg'], data['car']], axis=1)
xvar=sm.add_constant(xvar,prepend=True)
yvar=data['price']    
ols=sm.OLS(yvar,xvar).fit(cov_type = "HC0")
olscoef=ols.params
olsse=olscoef/ols.tvalues

##Q3
yvar=data['price']  
xvar=data['car']  

#a)
zvar_a1=data['weight'] 
xvar_a1=pd.concat([zvar_a1, xvar],axis =1)
xvar_a1=sm.add_constant(xvar_a1,prepend=True)
yvar_a1=data['mpg']
ols_a1=sm.OLS(yvar_a1,xvar_a1).fit()
mpg_hat1 = ols_a1.predict(xvar_a1)
nobs_a = xvar_a1.count().max()

#f-statistics = sqaure of t statistic
f_stat_a1 = ols_a1.tvalues.loc['weight']**2
f_stat_a1 = np.round(f_stat_a1,2)


xvar_a2=pd.concat([mpg_hat1,xvar],axis = 1)
xvar_a2=sm.add_constant(xvar_a2,prepend=True)
ols_a2=sm.OLS(yvar,xvar_a2).fit(cov_type = "HC0")
ols_param_a=ols_a2.params.to_numpy()
ols_param_a=np.round(ols_param_a,2)
ols_param_a=pd.DataFrame(ols_param_a)

#yeah finally found SE in OLS model!!
ols_se_a=ols_a2.HC0_se
ols_se_a = pd.Series(np.round(ols_se_a,2)) 
ols_se_a='(' +ols_se_a.map(str)+')'
ols_se_a=ols_se_a.reset_index(drop=True)


#b)
zvar_b1=data['weight']**2
xvar_b1=pd.concat([zvar_b1, xvar],axis = 1)
xvar_b1=sm.add_constant(xvar_b1,prepend=True)
yvar_b1=data['mpg']
ols_b1=sm.OLS(yvar_b1,xvar_b1).fit(cov_type = "HC0")
mpg_hat2 = ols_b1.predict(xvar_b1)
nobs_b = xvar_b1.count().max()

#f-statistics = sqaure of t statistic
f_stat_b1 = ols_b1.tvalues.loc['weight']**2
f_stat_b1 = np.round(f_stat_b1,2)

xvar_b2=pd.concat([mpg_hat2,xvar],axis = 1)
xvar_b2=sm.add_constant(xvar_b2,prepend=True)
ols_b2=sm.OLS(yvar,xvar_b2).fit(cov_type = "HC0")
ols_param_b=ols_b2.params.to_numpy()
ols_param_b=np.round(ols_param_b,2)
ols_param_b=pd.DataFrame(ols_param_b)

ols_se_b=ols_b2.HC0_se
ols_se_b = pd.Series(np.round(ols_se_b,2)) 
ols_se_b='(' +ols_se_b.map(str)+')'
ols_se_b=ols_se_b.reset_index(drop=True)

#c)
zvar_c1=data['height'] 
xvar_c1=pd.concat([zvar_c1, xvar],axis = 1)
xvar_c1=sm.add_constant(xvar_c1,prepend=True)
yvar_c1=data['mpg']
ols_c1=sm.OLS(yvar_c1,xvar_c1).fit(cov_type = "HC0")
mpg_hat3 = ols_c1.predict(xvar_c1)
nobs_c = xvar_c1.count().max()

#f-statistics = sqaure of t statistic
f_stat_c1 = ols_c1.tvalues.loc['height']**2
f_stat_c1 = np.round(f_stat_c1,2)

xvar_c2=pd.concat([mpg_hat3,xvar],axis = 1)
xvar_c2=sm.add_constant(xvar_c2,prepend=True)
ols_c2=sm.OLS(yvar,xvar_c2).fit()
ols_param_c=ols_c2.params.to_numpy()
ols_param_c=np.round(ols_param_c,2)
ols_param_c=pd.DataFrame(ols_param_c)

ols_se_c=ols_c2.HC0_se
ols_se_c = pd.Series(np.round(ols_se_c,2)) 
ols_se_c='(' +ols_se_c.map(str)+')'
ols_se_c=ols_se_c.reset_index(drop=True)


#creating a table!
col_a=pd.concat([ols_param_a,ols_se_a], axis = 1).stack()
col_a=col_a.append(pd.Series(f_stat_a1))
col_a=col_a.append(pd.Series(nobs_a))

col_b=pd.concat([ols_param_b,ols_se_b], axis = 1).stack()
col_b=col_b.append(pd.Series(f_stat_b1))
col_b=col_b.append(pd.Series(nobs_b))

col_c=pd.concat([ols_param_c,ols_se_c], axis = 1).stack()
col_c=col_c.append(pd.Series(f_stat_c1))
col_c=col_c.append(pd.Series(nobs_c))

rownames =pd.concat([pd.Series(['constant','mpg','car(sedan)','F-statistic','Observations']),pd.Series([' ',' ',' ',])],axis = 1).stack()
colnames = pd.Series(['(a)','(b)', '(c)'])

table1 = pd.concat([col_a, col_b, col_c], axis=1)
table1.index = rownames
table1.columns = colnames

table1.to_latex('table1_python.tex') 

##Q4
GMM_4 = IVGMM.from_formula('price ~ 1 + car + [mpg ~ weight]',data).fit()
#default: robust SE
GMM_param=pd.DataFrame(GMM_4.params.to_numpy())
GMM_param=np.round(GMM_param,2)

#how can I get SE from IVGMM...?
GMM_ci=GMM_4.conf_int()
GMM_ci=pd.DataFrame(np.round(GMM_ci,2))
ci_GMM = '(' + GMM_ci['lower'].map(str) + ', ' + GMM_ci['upper'].map(str) + ')'
ci_GMM=ci_GMM.reset_index(drop=True)
col_GMM=pd.concat([GMM_param,ci_GMM], axis = 1).stack()
rownames =pd.concat([pd.Series(['constant','car','mpg']),pd.Series([' ',' ',' ',])],axis = 1).stack()
col_GMM.index=rownames

col_GMM.to_latex('table2_python.tex') 


