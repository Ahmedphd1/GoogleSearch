import string
import xml.etree.ElementTree as ET
import hashlib
import requests
import time
import json
import threading

unique_list = []
keyword_list = []
list_a = []
k_list = []

# Creating a list and adding the keywords list here so that we dont need to run the function again
indexlist_threading = []

# adding the multiple parsed list here
local_list_threading = []

key = input("Enter a KeyWord: ").lower()

list_b = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
		   "ü", "ä", "ö"] 
prefix_list = ["is", "is not", "isn\'t", "are", "are not", "aren\'t", "did", "did not", "didn\'t", "will", "won\'t", "will not", "do", "do not", "don\'t", "have", "have not", "haven\'t", "has", "has not", "hasn\'t", "Can", "can not", "can\'t", "should", "should not", "shouldn\'t", "could", "could not", "couldn\'t", "would", "would not", "wouldn\'t", "does", "does not", "doesn\'t", "was", "was not", "wasn\'t", "How", "if", "who", "where", "why", "what", "when", "which", "Best", "Won\'t", "Why do", "Can you", "What to do with", "What do"]
		   



# secret = '2gydm0SGnm9WAPbHB1pBVf'
# params = {
# 	"license": "PD9812042CDDAF056",
# 	"time": int(time.time()),
# 	"cnt": 2,
# }
# params["sign"] = hashlib.md5((params["license"] + str(params["time"]) + secret).encode('utf-8')).hexdigest()
# try:
#
# 	# Step 1 : Obtain proxy IP
# 	# Important: the ip addresses in the obtained ip:port list belong to ip.cheap central server, NOT the proxy node ip which finally communicate with the target server.
# 	response = requests.get(
# 		url="https://api.ip.cheap/v1/obtain",
# 		params=params,
# 		headers={
# 			"Content-Type": "text/plain; charset=utf-8",
# 			"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64, x64, rv:83.0) Gecko/20100101 Firefox/83.0"
# 		},
# 		data="1"
# 	)
# 	# print('Response HTTP Status Code: {status_code}'.format(
# 	# status_code=response.status_code))
# 	# print('Response HTTP Response Body: {content}'.format(
# 	# content=response.content))
#
# 	# Step 2 : Use proxy IP
# 	try:
# 		res = json.loads(response.content)
# 		proxies = {
# 			"http"  : "http://" + res['data']['proxies'][0],
# 			"https" : "http://" + res['data']['proxies'][0],
# 		}
#
# 		# return proxies
# 	except Exception as e:
# 		pass
	
# except requests.exceptions.RequestException:
# 	print('HTTP Request failed')
#
# 	# return proxies


def proxy_threading():
	secret = '2gydm0SGnm9WAPbHB1pBVf'
	params = {
		"license": "PD9812042CDDAF056",
		"time": int(time.time()),
		"cnt": 100,
		"iso": "US",  # the proxy is now only "us" proxies
	}

	params["sign"] = hashlib.md5((params["license"] + str(params["time"]) + secret).encode('utf-8')).hexdigest()

	try:
		response = requests.get(url="https://api.ip.cheap/v1/obtain",params=params,headers={
				"Content-Type": "text/plain; charset=utf-8",
				"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64, x64, rv:83.0) Gecko/20100101 Firefox/83.0"
			},
			data="1"
		)

		res = json.loads(response.content)

		proxies = {
			"https": "https://" + res['data']['proxies'][0],
			# i have deleted the "http" proxy because the website only accepts "https" that is why the proxy was not working
		}

		print("proxy found: {0}".format(proxies))



	except:
		print("proxy not found: trying again")
		proxy_threading()
	return proxies

def list_add(list_z):
	global indexlist_threading

	list_c = [f"{key} {j}" for j in list_z]
	list_3 = [f"{x} {y}" for x in prefix_list for y in list_c ]
	indexlist_threading = list_3 # adding the list_3 to the global indexlist_threading so that we can use it later on
	return list_3
	
def keyword_parsing(list_x):
	local_list = []
	global proxies

	for x in list_x:
		print(x)

		targrtUrl = "http://suggestqueries.google.com/complete/search?output=toolbar&hl=de&q=" + x
		r = requests.get(url=targrtUrl, proxies=proxies) # still using session to get the target data from the website
		print('Response HTTP Status Code: {status_code}'.format(status_code=r.status_code))
		
		if r.status_code == 200:
			try:
				tree = ET.fromstring(r.text)
				 
				for child in tree.iter('suggestion'):
					local_list.append(child.attrib['data'])
					print(child.attrib['data'])
			except Exception as e:
				pass
		else:
			# i += 1
			pass
			
	return local_list


# a  copy of the keyword_parsing function but this function takes the index position of the list
def keyword_parsing_threading(indexposition):
	local_list = []
	global proxies
	global local_list_threading
	global indexlist_threading


	URL = "http://suggestqueries.google.com/complete/search?output=toolbar&hl=de&q=sadsadsa"

	targrtUrl = "http://suggestqueries.google.com/complete/search?output=toolbar&hl=de&q=" + indexlist_threading[indexposition] # adding the value in the list to the url

	print(indexposition)
	s = requests.session()  # creating a session request because the request to the website need to be kept "alive" instead of just 1 quick request
	s.headers.update({'user-agent': URL})  # retrieving the headers from the website and assigning it to the headers parameter

	r = s.get(url=targrtUrl, proxies=proxy_threading())
	print('Response HTTP Status Code: {status_code}'.format(status_code=r.status_code))

	if r.status_code == 200:
		try:
			tree = ET.fromstring(r.text)
			print("request successful")

			for child in tree.iter('suggestion'):
				local_list.append(child.attrib['data'])
				local_list_threading.append(child.attrib['data']) # appending the results to the local_list //note this list is not ordered//
				print(child.attrib['data'])
		except Exception as e:
			print("could not find any data")
			pass
	else:
		# i += 1
		print("Request not successful: Trying again")


	return local_list

def threadingfunction(): # the threading function that has to be run after we retrieve the list_3
	global indexlist_threading
	for x in range(len(indexlist_threading)):
		time.sleep(0.2)
		print(x)
		api_thread = threading.Thread(target=keyword_parsing_threading, args=(x,))
		api_thread.start()

def unique_list_creator(list1, list2):
	 return list(set(list1).union(set(list2)))

def list_broker(list_d):
	new_list = []
	# y = keyword_parsing(list_c)

	for j in list_d:
		new_list.extend(j.split())
	return new_list

def data_list(list_aa, list_bb):
	local_list = []
	if len(list_aa) == 0:
		return list_bb
	else:
		for i in list_bb:
			if i not in list_aa:
				local_list.append(i)
		return local_list

