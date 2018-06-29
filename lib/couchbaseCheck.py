from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery
from robot.api import logger
import time

def success(item):
    info = item + " exists in Couchbase Server"
    logger.console(info)
    logger.info(info)

def fail(item):
    info = item + " does not exist in Couchbase Server"
    logger.error(info)

def match_couchbase_item_details(row, col, items, column_names):
    '''
    Creates a keyword named "Match Couchbase Item Details"
    This keyword takes four arguments, number of rows and columns in list
    of items, list of items itself, and excel file's column names.
    Returns boolean value whether the specified N1QL query found result or not,
    and log its result whether error occurs or not.
    '''
    
    timeout = time.time() + 60

    cluster = Cluster('couchbase://10.99.143.96:8091')
    authenticator = PasswordAuthenticator('Administrator', 'password')
    cluster.authenticate(authenticator)
    cb = cluster.open_bucket('item')

    for i in range(row):
        for j in range(col):

            sku = items[i][0]
            key_name = column_names[j]
            check = items[i][j]
            results = []
            found = False       # set the flag

            while not found:

                key_name = str(key_name)
                key_name = key_name.lower()

                if (sku == check):
                    q = "SELECT * FROM `item` WHERE code='" + str(sku) + "'"

                elif ("package" in key_name) or ("inner" in key_name) or ("outer" in key_name):
                    # Example querying nested object:
                    # SELECT * FROM `item` WHERE code='QRTS00001' and size.`inner`.length=300

                    key_parse = key_name.split(" ")

                    if "category" in key_parse[1]:
                        key_parse[1] = "size_" + key_parse[1]
                        check = "'" + str(check) + "'"

                    if ("inner" in key_name) or ("outer" in key_name):
                        q = "SELECT * FROM `item` WHERE code='" + str(sku) + "' AND size.`" + str(key_parse[0]) + "`." + str(key_parse[1]) + "=" + str(check)
                    else:
                        key_parse[0] += "s"
                        q = "SELECT * FROM `item` WHERE code='" + str(sku) + "' AND size.`" + str(key_parse[0]) + "`." + str(key_parse[1]) + "=" + str(check)
                    
                else:
                    # Handle different column names
                    if ("full/part" in key_name):
                        key_name = "type"
                        check = check.lower()
                    if ("handling list" in key_name):
                        key_name = "handling_list"

                    # Query with its primary key
                    q = "SELECT * FROM `item` WHERE code='" + str(sku) + "' AND " + str(key_name) + "='" + str(check) + "'"

                query = N1QLQuery(q)
                for row in cb.n1ql_query(query):
                    results.append(row)

                temp_msg = str(sku) + ": " + str(check)
                if (len(results) > 0):
                    found = True
                    if (j == 0):
                        success(temp_msg)

                if time.time() > timeout:
                    # error message
                    fail(item)
                    break
                
    return True