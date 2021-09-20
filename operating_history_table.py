import pandas as pd
from bs4 import BeautifulSoup
import requests

#Data is not available in a ready-to-use format, need to do some webscraping
baseURL = 'https://pris.iaea.org/PRIS/CountryStatistics/ReactorDetails.aspx?current='

main_tables_list = []
reactor_details_list = []

headers = {
    'User-Agent': 'Personal project; Peter Oravecz',
    'From': 'peteroravecz94@gmail.com'
}

#The URL of reactor details simply ends in the index number of the reactor. This  seems to be an arbitrary 3 digit number.
for i in range(1,4):
	##Parsing HTML to find country and reactor name, html tables
	cur_url = baseURL + str(i)
	cur_html = requests.get(cur_url, headers = headers).text
	soup = BeautifulSoup(cur_html, 'html.parser')
	#Some reactor index numbers are not populated, those URLs return an error page
	if soup.find('div', id='content').h3.text.strip() != "Unauthorized Access" or soup.find('div', id='content').h3.text.strip() != "Unexpected Problem Occurred":
		tables = pd.read_html(cur_html)

		reactor_name = soup.find('span', id='MainContent_MainContent_lblReactorName').b.text.strip()
		country_name = soup.find('a', id='MainContent_litCaption').text.strip()

		##Amending main data table with country and reactor names
		tables[2]["Country"] = country_name
		tables[2]["Reactor_name"] = reactor_name

		#Add main table data to list
		main_tables_list = main_tables_list + tables[2].values.tolist()

		#Add reactor details to list
		current_detail = [tables[0][0][1],tables[0][1][1],tables[0][1][3],tables[0][0][5], tables[0][1][7],tables[0][2][1],tables[0][3][1],country_name,reactor_name]
		reactor_details_list.append(current_detail)
	else:
		print("Reactor ID: (" + str(i) + ") did not return a valid page.")

reactor_details_df = pd.DataFrame(reactor_details_list, columns=[
	"reactor_Type", 
	'model', 
	'design_net_capacity', 
	'construction_start_date', 
	"commercial_operation_date", 
	"owner", 
	"operator", 
	"country", 
	"reactor_name"])

main_tables_df = pd.DataFrame(main_tables_list, columns = [
	"Year", 
	"Electricity Supplied [GW.h]", 
	"Reference Unit Power [MW]", 
	"Annual Time On Line [h]", 
	"Operation Factor [%]", 
	"Annual Energy Availability Factor [%]", 
	"Cumulative Energy Availability Factor [%]", 
	"Annual Load Factor [%]", 
	"Cumulative Load Factor [%]", 
	"country", 
	"reactor_name"])

main_tables_df.to_csv(path_or_buf = "main_tables_output.csv")
reactor_details_df.to_csv(path_or_buf = "reactor_details_output.csv")