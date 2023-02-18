
* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	local outputpath = "/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework5/output" 
	
		cd "`outputpath'"

	ssc install weakivtest
	ssc install avar	

********************************************************************************
* Fit linear regression model

	import delimited "/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework5/instrumentalvehicles.csv" 
	
	ivregress liml price car (mpg = weight car), vce(robust)
	
	weakivtest, level(0.05)
	
	outreg2 using table1_stata.tex


