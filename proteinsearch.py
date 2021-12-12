# Automated Antibody Search
# Kaitlin Sullivan - UBC March 2020

# This code uses selenium webdriver to automate search for antibodies based on marker genes found via scRNA-seq
# Input: a dataframe containing uniquely upregulated marker genes for a given cluster

# REQUIREMENTS: 
# Download selenium in terminal using the command: pip install selenium
# Download Chrome driver via https://chromedriver.chromium.org/downloads
# Input the file path for chromedriver on LINE 42


###############SET UP#################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


import pandas as pd

# create a data frame with info to save regarding astrocyte protein expression
co = ["Gene", "FullName", "Region", "Antibody", "Neurons", "Glia", "pct1", "pct2"]
df = pd.DataFrame(columns=co)

# get user input for which file to open
toOpen = input("Enter the file path of your marker gene csv file: ")

# save whole df
markers = pd.read_csv(toOpen)

# save all gene names to iterate through
allgenes = markers['Unnamed: 0']
# save the pct values
pct1 = markers['pct.1']
pct2 = markers['pct.2']

# get user input for what to name the new file
toSave = input("Enter the name you would like to save the output file as (be sure to include .csv at the end): ")
   
# this line will open up your controlled chrome window
# input the filepath of your chromedriver here
driver = webdriver.Chrome("/Users/kaitlinsullivan/opt/miniconda3/lib/python3.8/site-packages/chromedriver")

# open protein atlas (or any website of choice)
driver.get("https://www.proteinatlas.org/")

##############SEARCH FOR GENES IN LIST#################

# loop through each each and search for protein expression in the hippocampus and cortex
for z in range(len(allgenes)):
	cur_gene = allgenes[z]
	cur_pct1 = pct1[z]
	cur_pct2 = pct2[z]

	# locate the search bar and submit button
	# if you are looking to use this code for a different website:
	# go to that website and press option+command+U - this will bring up the source code so you can find elements
	search_bar = driver.find_element_by_id("searchQuery")
	sub_button = driver.find_element_by_id("searchButton")

	# search gene names via imported marker gene list
	search_bar.clear()
	search_bar.send_keys(cur_gene)
	sub_button.click()

	# get the full gene name 
	# this searches for the second HTML element of the table that pops up after searching a given gene name
	# since the gene of choice may not always be at the top of the list, best to iterate through list
	cur_names = driver.find_elements_by_class_name("tda")
	
	# if there are no genes found skip to next iteration
	if(len(cur_names)==0):
		continue

	# iterate through list of gene names to find gene in question
	i = 0
	exist = True
	while(cur_names[i].text != cur_gene):
		i+=1
		if(i>=len(cur_names)):
			exist = False
			break

	# if the search results do not bring up the gene name, skip to next iteration
	if(exist != True):
		continue
		
	#save the full name of the gene
	cur_name = cur_names[i+1].text

##############GET BRAIN TISSUE INFO###################
	
	# select brain tissue protein expression by finding correct gene HTML element
	gene_xpath = "//a[contains(@href, '-" + cur_gene + "/brain')]"
	brain = driver.find_elements_by_xpath(gene_xpath)

	# if there is no brain tissue info skip
	if(len(brain)==0):
		cur_region = "NA"
		cur_a = "NA"
		cur_neur = "NA"
		cur_glia = "NA"

		# write empty line for gene
		cur = pd.DataFrame([[cur_gene, cur_name, cur_region, cur_ab, cur_neur, cur_glia, cur_pct1, cur_pct2]], columns=co)
		df.append(cur, ignore_index=True)
		continue

		
	brain[0].click()

	# select tissue menu
	tissue = driver.find_element_by_class_name("tissue_menu_opener")
	tissue.click()

	# save all tissue types in a list
	tissue = driver.find_elements_by_xpath("//div/span/a/span")

	# convert from web elements to strings
	tissue_text = [None]*len(tissue)
	for y in range(len(tissue)):
		tissue_text[y] = tissue[y].text

##############CEREBRAL CORTEX###################
	
# save cortical info
	if("CEREBRAL CORTEX" in tissue_text):
		
		# click on the hippocampus
		cortex = driver.find_elements_by_xpath("//a[contains(@href, '/cerebral+cortex')]")
		cortex[0].click()
		cur_region = "Cortex"

		# save antibody names as a list
		ab_h = driver.find_elements_by_class_name("head_nohex")

	##### if there are no antibodies
		if(len(ab_h)==0):
			cur_ab = "NA"
			cur_neur = "NA"
			cur_glia = "NA"

			# write empty line for gene in HC
			cur = pd.DataFrame([[cur_gene, cur_name, cur_region, cur_ab, cur_neur, cur_glia, cur_pct1, cur_pct2]], columns=co)
			df = df.append(cur, ignore_index=True)
			
	##### if there are antibodies
		else:
			# find parent element of table holding values
			parent = driver.find_element_by_xpath("//table[@class='border dark']") 
			# find the values
			cells = parent.find_elements_by_tag_name("td")

				
			for x in range(len(ab_h)):
				
				# manually check that there are 4 variables as assumed
				if(len(cells)<4):
					# save line to table
					cur = pd.DataFrame([[cur_gene, cur_name, cur_region, cur_ab, "check", "check", cur_pct1, cur_pct2]], columns=co)
					df = df.append(cur, ignore_index=True)
						
				else:
					cur_ab = ab_h[x].text
					cur_glia = cells[len(ab_h)+x].text
					cur_neur = cells[(len(ab_h)*2)+x].text
					
					#save line to table
					cur = pd.DataFrame([[cur_gene, cur_name, cur_region, cur_ab, cur_neur, cur_glia, cur_pct1, cur_pct2]], columns=co)
					df = df.append(cur, ignore_index=True)


##############HIPPOCAMPAL FORMATION###################
# save hippocampal info
	if("HIPPOCAMPAL FORMATION" in tissue_text):
		if("CEREBRAL CORTEX" in tissue_text):
			# open tissue menu
			tissue = driver.find_element_by_class_name("tissue_menu_opener")
			tissue.click()
		# click on the hippocampus
		hippo = driver.find_elements_by_xpath("//span[@title='Hippocampal formation']")
		hippo[0].click()			
		cur_region = "Hippocampus"

		# save antibody names as a list
		ab_h = driver.find_elements_by_class_name("head_nohex")

	##### if there are no antibodies
		if(len(ab_h)==0):
			cur_a = "NA"
			cur_neur = "NA"
			cur_glia = "NA"
	
			# write empty line for gene in HC
			cur = pd.DataFrame([[cur_gene, cur_name, cur_region, cur_ab, cur_neur, cur_glia, cur_pct1, cur_pct2]], columns=co)
			df = df.append(cur, ignore_index=True)
			
	##### if there are antibodies
		else:
			# find parent element of table holding values
			parent = driver.find_element_by_xpath("//table[@class='border dark']") 
			# find the values
			cells = parent.find_elements_by_tag_name("td")

			for x in range(len(ab_h)):
				cur_ab = ab_h[x].text
				cur_glia = cells[x].text
				cur_neur = cells[len(ab_h)+x].text
						
				#save line to table
				cur = pd.DataFrame([[cur_gene, cur_name, cur_region, cur_ab, cur_neur, cur_glia, cur_pct1, cur_pct2]], columns=co)
				df = df.append(cur, ignore_index=True)

	
				
# write df to file
df.to_csv(toSave, index=False)

# close the browser
driver.quit()
print("Protein search complete :)")

