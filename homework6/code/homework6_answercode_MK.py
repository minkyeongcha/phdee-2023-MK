#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Clear all

from IPython import get_ipython
get_ipython().magic('reset -sf')

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Set working directories and seed

outputpath = os.chdir('/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework6/output')
data=pd.read_csv('/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework6/instrumentalvehicles.csv')

###Q2
plt.scatter(data['length'], data['mpg'], alpha=0.5)
plt.xlabel("length")
plt.ylabel("mpg")
plt.vlines(x=225, ymin=0, ymax=55, colors="black", linestyle='dashed')
plt.savefig("scatterplot.png")
nobs=data.count().max()

###Q3
x_tilda=data['length']-225 
data['D']=np.empty([nobs, 1]) 
for r in range(nobs):
    if x_tilda[r]<0 : data['D'][r]=0
    else: data['D'][r]=1

yvar=data['mpg']

xvar1=pd.concat([x_tilda, data['D'],  data['D']*x_tilda], axis=1)

ols_3=sm.OLS(yvar,sm.add_constant(xvar1,prepend=True)).fit(cov_type = "HC0")
ols_param_3=ols_3.params.to_numpy()
ols_se_3=ols_3.HC0_se

x_a = np.linspace(x_tilda.min(),0,100)
x_b = np.linspace(0,x_tilda.max(),100)

y_3a = ols_param_3[0] + ols_param_3[1]*x_a
y_3b = ols_param_3[0] + (ols_param_3[1]+ols_param_3[3])*x_b + ols_param_3[2] 

plt.scatter(x_tilda, data['mpg'],facecolors='none', edgecolors='grey')
plt.plot(x_a,y_3a)
plt.plot(x_b,y_3b)
plt.vlines(x=0, ymin=0, ymax=55, colors="black", linestyle='dashed')
plt.xlabel("length_cutoff")
plt.ylabel("mpg")
plt.savefig("plot_Q3.png")


##Q4
xvar2=pd.concat([x_tilda, x_tilda**2, data['D'], data['D']*x_tilda, data['D']*(x_tilda**2)], axis=1)
ols_4=sm.OLS(yvar,sm.add_constant(xvar2,prepend=True)).fit(cov_type = "HC0")
ols_param_4=ols_4.params.to_numpy()
ols_se_4=ols_4.HC0_se
np.round(ols_4.pvalues,2)

y_4a = ols_param_4[0] + ols_param_4[1]*x_a + ols_param_4[2]*(x_a**2)
y_4b = ols_param_4[0] + (ols_param_4[1]+ols_param_4[4])*x_b + (ols_param_4[2]+ols_param_4[5])*(x_b**2) + ols_param_4[3]

plt.scatter(x_tilda, data['mpg'],facecolors='none', edgecolors='grey')
plt.plot(x_a,y_4a)
plt.plot(x_b,y_4b)
plt.vlines(x=0, ymin=0, ymax=55, colors="black", linestyle='dashed')
plt.xlabel("length_cutoff")
plt.ylabel("mpg")
plt.savefig("plot_Q4.png")


##Q5
xvar3=pd.concat([x_tilda, x_tilda**2, x_tilda**3, x_tilda**4, x_tilda**5, data['D'], data['D']*x_tilda, data['D']*x_tilda**2, data['D']*x_tilda**3, data['D']*x_tilda**4, data['D']*x_tilda**5], axis=1)
ols_5=sm.OLS(yvar,sm.add_constant(xvar3,prepend=True)).fit(cov_type = "HC0")
ols_param_5=ols_5.params.to_numpy()
ols_se_5=ols_5.HC0_se
np.round(ols_5.pvalues,2)

y_5a = ols_param_5[0] + ols_param_5[1]*x_a + ols_param_5[2]*(x_a**2)+ ols_param_5[3]*(x_a**3)+ ols_param_5[4]*(x_a**4)+ols_param_5[5]*(x_a**5)
y_5b = ols_param_5[0] + (ols_param_5[1]+ols_param_5[7])*x_b + (ols_param_5[2]+ols_param_5[8])*(x_b**2) + (ols_param_5[3]+ols_param_5[9])*(x_b**3) + (ols_param_5[4]+ols_param_5[10])*(x_b**4) + (ols_param_5[5]+ols_param_5[11])*(x_b**5) +  ols_param_5[6]

plt.scatter(x_tilda, data['mpg'],facecolors='none', edgecolors='grey')
plt.plot(x_a,y_5a)
plt.plot(x_b,y_5b)
plt.vlines(x=0, ymin=0, ymax=55, colors="black", linestyle='dashed')
plt.xlabel("length_cutoff")
plt.ylabel("mpg")
plt.savefig("plot_Q5.png")


##combining all 
ols_param_3=np.round(ols_param_3,2)
ols_param_4=np.round(ols_param_4,2)
ols_param_5=np.round(ols_param_5,2)

ols_param_3=pd.DataFrame(ols_param_3)
ols_param_4=pd.DataFrame(ols_param_4)
ols_param_5=pd.DataFrame(ols_param_5)

ols_se_3 = pd.Series(np.round(ols_se_3,2)) 
ols_se_3='(' +ols_se_3.map(str)+')'
ols_se_3=ols_se_3.reset_index(drop=True)

ols_se_4 = pd.Series(np.round(ols_se_4,2)) 
ols_se_4='(' +ols_se_4.map(str)+')'
ols_se_4=ols_se_4.reset_index(drop=True)

ols_se_5 = pd.Series(np.round(ols_se_5,2)) 
ols_se_5 ='(' +ols_se_5.map(str)+')'
ols_se_5=ols_se_5.reset_index(drop=True)

#creating a table!
col_3=pd.concat([ols_param_3,ols_se_3], axis = 1).stack()
col_3=col_3[2]
col_3=col_3.append(pd.Series(nobs))

col_4=pd.concat([ols_param_4,ols_se_4], axis = 1).stack()
col_4=col_4[3]
col_4=col_4.append(pd.Series(nobs))

col_5=pd.concat([ols_param_5,ols_se_5], axis = 1).stack()
col_5=col_5[6]
col_5=col_5.append(pd.Series(nobs))

rownames =pd.concat([pd.Series(['treatment effect','Observations']),pd.Series([' '])],axis = 1).stack()
colnames = pd.Series(['(Q3)','(Q4)', '(Q5)'])

table1 = pd.concat([col_3, col_4, col_5], axis=1)
table1.index = rownames
table1.columns = colnames

table1.to_latex('/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework6/output/table1_python.tex') 

###Q6
zvar=data['mpg'] 

xvar_6a=xvar1
xvar_6a=sm.add_constant(xvar_6a,prepend=True)

ols_6a=sm.OLS(zvar,xvar_6a).fit(cov_type = "HC0")
ols_param_6a=ols_6a.params.to_numpy()
mpg_hat1 = ols_6a.predict(xvar_6a)

#f-statistics = sqaure of t statistic
f_stat = ols_6a.tvalues.loc['D']**2
f_stat = np.round(f_stat,2)

xvar_6b=pd.concat([mpg_hat1,data['car']],axis = 1)
xvar_6b=sm.add_constant(xvar_6b,prepend=True)
yvar2=data['price']
ols_6b=sm.OLS(yvar2,xvar_6b).fit(cov_type = "HC0")
np.round(ols_6b.params.to_numpy(),2)


