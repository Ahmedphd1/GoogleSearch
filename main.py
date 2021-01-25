from datetime import datetime
import test as func
import time
import numpy as np
from database import *
import pymongo


startTime = datetime.now()
unique_list = []

def runscript(): # creating a runscript function
    func.list_add(func.list_b) # Running the list_add function but does not return anything because our list is global!

    func.threadingfunction() # running the threading function that send a request to google containing the keywords

    time.sleep(5) # sleeping for 5 seconds so that all the data can be collected

    keyword_list = func.local_list_threading # assigning the list we created!

    keyword_list = list(set(keyword_list))

    print("this is the keyword list: {0}".format(keyword_list))

    if len(keyword_list) > 0:
        _list = data_list(unique_list, keyword_list)

        for i in _list:
            insert_db(i)
        unique_list.extend(i)
        list_b.clear()
        list_b = (list(set(list_broker(_list))))
    else:
        print("List is 0")


print("Total time elapsed: ", datetime.now() - startTime)


runscript() # running the script
