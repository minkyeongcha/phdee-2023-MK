
* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	local outputpath = "/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework7/output" 
	
		cd "`outputpath'"

********************************************************************************
* Fit linear regression model

	generate tr = 0
	replace tr = 1 if ((year==2020) & (month != 1)& (month != 2)) 
	
	generate ln_mw = log(mw)
	encode zone, generate(zone2)
	
	reg ln_mw i.zone2#i.month#i.dow#i.hour tr temp pcp, vce(robust)

	generate month2 = .
	replace month2 = month if  ((month!= 1) & (month!=2))

	teffects nnmatch (ln_mw temp pcp i.zone2 i.dow i.hour i.month2) (tr), nneighbor(1) ematch(zone2 dow hour month2) vce(robust) atet
	
	
	keep if ((year==2018)|(year==2019)|(year==2020))
	reg ln_mw i.zone2#i.month#i.dow#i.hour#i.year tr temp pcp, vce(robust)
* not working.... 

	generate year_2020 = 0
	replace year_2020 = 1 if (year==2020)
	
	keep if ((year==2019)|(year==2020))
	
	teffects nnmatch (ln_mw temp pcp i.zone2 i.dow i.hour i.month) (year_2020), nneighbor(1) ematch(zone2 dow hour month) vce(robust) generate(stub)
	predict y_hat, po

	keep if (year==2020)
	generate y = ln_mw - y_hat
	
	reg y tr, vce(robust)
	
	outreg2 using table1_stata.tex


