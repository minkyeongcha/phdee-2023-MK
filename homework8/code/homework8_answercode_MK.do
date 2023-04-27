
* Start by clearing everything

	clear all 
	set more off

* Set up your working directories

	local outputpath = "/Users/mk/Desktop/Spring 2023/Environment Econ 2/homeworks/phdee-2023-MC/homework8/output" 
	
		cd "`outputpath'"

********************************************************************************
* Q1 

	set maxvar 120000
	
	gen tr = 0
	replace tr = 1 if nyc==1 
	
	egen recycle_tr = mean(recyclingrate) if tr==1
	
	preserve
	collapse(mean) recyclingrate, by (tr year)
	reshape wide recyclingrate, i(year) j(tr)
	graph twoway line recyclingrate* year, yscale(r(0 0.4)) sort ytitle("Recycling Rate") legend(order(1 "Controls" 2 "NYC"))
	restore
	
*Q2
	gen pause=0
	replace pause=1 if ((year == 2002)| (year == 2003)|(year == 2004))
	
	egen region_dummy = group(region)
	
	preserve
	drop if year >=2005
	reg recyclingrate tr##pause i.region_dummy i.year, vce(cluster region_dummy)
	outreg2 using results, keep (tr##pause) tex(nopretty) replace

	reg recyclingrate tr##pause incomepercapita collegedegree2000 nonwhite democratvoteshare2000 democratvoteshare2004 i.region_dummy i.year, vce(cluster region_dummy)
	outreg2 using results, keep (tr##pause incomepercapita collegedegree2000 nonwhite democratvoteshare2000 democratvoteshare2004) tex(nopretty) word append

	outreg2 using table1_stata.tex
	restore
	
*Q3
	ssc install sdid, replace
	gen treated=tr*pause
	
	preserve
	drop if year >=2005
	sdid recyclingrate region_dummy year treated, vce(placebo) graph g2_opt(ylabel(0 0.4) xlabel(1995(5)2005) ytitle("Recycling Rate")scheme(plotplainblind)) graph_export(sdid_, .pdf)
	
	
	eststo sdid_1: sdid recyclingrate region_dummy year treated, vce(placebo) 
	eststo sdid_2: sdid recyclingrate region_dummy year treated, vce(placebo) covariates(incomepercapita collegedegree2000 nonwhite democratvoteshare2000 democratvoteshare2004)

	esttab sdid_1 sdid_2 using table2_stata.tex, starlevel ("*" 0.10 "**" 0.05 "***" 0.01) b(%-9.3f) se(%-9.3f)
	restore
	
*Q4
	reg recyclingrate tr#i.year incomepercapita collegedegree2000 nonwhite democratvoteshare2000 democratvoteshare2004 i.region_dummy i.year if year!=2001,  vce(cluster region_dummy)
	
	coefplot, keep(1.tr#*.year) base vertical coeflabels(1.tr#1997.year = "1997" 1.tr#1998.year = "1998" 1.tr#1999.year = "1999" 1.tr#2000.year = "2000" 1.tr#2002.year = "2002" 1.tr#2003.year = "2003" 1.tr#2004.year = "2004" 1.tr#2005.year = "2005" 1.tr#2006.year = "2006" 1.tr#2007.year = "2007" 1.tr#2008.year = "2008") yscale(r(-0.12, 0.1)) xline(4.5) yline(0, lcolor("106 208 200")) 
	
	outreg2 using table3_stata.tex, keep (tr#i.year incomepercapita collegedegree2000 nonwhite democratvoteshare2000 democratvoteshare2004) tex(nopretty) replace
	
*Q5
	replace region_dummy = 500 if nyc==1 
	duplicates drop region_dummy year, force
	tsset region_dummy year
	
	*ssc install distinct, replace all
	*ssc install elasticregress, replace all
	*ssc install blindschemes, replace all
	*net install tsg_schemes, from("https://raw.githubusercontent.com/asjadnaqvi/Stata-schemes/main/schemes/") replace
	*ssc install synth, replace all
	*net install synth_runner, from("https://raw.github.com/bquistorff/synth_runner/master/") replace all
	net install allsynth, from("https://justinwiltshire.com/s") replace all
	
	synth_runner recyclingrate munipop2000 incompercpita collegedegree2000 nonwhite, trunit(500) trperiod(2002&2003&2004) gen_vars
	
	
	


