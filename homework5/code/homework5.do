* Sample Stata code -- Dylan Brewer

* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	local outputpath = "/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework4/output" 
	
		cd "`outputpath'"

	
* Download and use plotplainblind scheme

	ssc install blindschemes, all
	set scheme plotplainblind, permanently
	

********************************************************************************
* Fit linear regression model

	import delimited "/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework4/fishbycatch.txt" 
	
	reshape long salmon shrimp bycatch, i(firm) j(month)  

	generate tr = 0
	replace tr = 1 if treated & month < 13
	
	reg bycatch i.firm i.month  tr firmsize salmon shrimp,noconstant vce(cluster firm)
	
	foreach v of varlist bycatch firmsize salmon month shrimp tr {
	bysort firm: egen mean_`v'=mean(`v')
	g dem_`v'=`v'-mean_`v'
	drop mean_`v'
	}
	
	reg bycatch i.firm i.month  tr firmsize salmon shrimp,noconstant vce(cluster firm)
	outreg2 using results, keep (tr firmsize salmon shrimp) tex(nopretty) replace

	reg dem_bycatch tr dem_salmon dem_shrimp,noconstant vce(cluster firm)
	outreg2 using results, keep (tr dem_salmon dem_shrimp) tex(nopretty) word append
	
	
		
