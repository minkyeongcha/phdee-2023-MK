
* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	local outputpath = "/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework6/output" 
	
		cd "`outputpath'"

	ssc install avar	
	ssc install rdrobust

********************************************************************************
* Fit linear regression model

	import delimited "/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework6/instrumentalvehicles.csv" 
	
	generate tr = 0
	replace tr = 1 if length >= 225
	
	generate xtilda=length-225
	
	rdrobust mpg xtilda, c(0) bwselect(mserd) vce(hc0)	
	
	rdplot mpg xtilda, nbins(20 20) c(0) p(1) genvars
	
	reg price rdplot_hat_y car
	
	outreg2 using table1_stata.tex

	rdplot mpg xtilda, c(0) p(1)
	graph export


