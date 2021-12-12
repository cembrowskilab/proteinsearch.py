# proteinsearch.py  
An automated web search for human antibodies labelling neurons and glia in the brain.   
This code takes the direct output of Seurat's `FindMarkers()` and returns a data frame of antibodies based on information from the human protein atlas.  


## Instructions:  
1. Save a `.csv` of the marker genes for your single cell RNA sequencing data: `write.csv(FindMarkers(data), markers.csv)`
2. In your terminal, ensure that Selenium web driver is installed: `pip install selenium`
3. Download Chrome driver [here](https://chromedriver.chromium.org/downloads).
4. In the terminal, navigate to the directory holding `proteinsearch.py`.
5. In the terminal, type: `python proteinsearch.py`
6. Enter the absolute path of your marker gene csv.
7. Enter the name of of the output file (be sure to include .csv at the end).
8. Chrome driver will open and begin the search!
