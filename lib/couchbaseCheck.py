from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery
from robot.api import logger

def write(s):
    logger.console(s)

def check_in_couchbase(sku, key_name, check):
    '''
    Creates a keyword named "Check In Couchbase"
    This keyword takes three arguments, sku as primary key, key identifier, 
    and value to be checked inside couchbase server, Returns boolean value 
    whether the specified N1QL query found result or not.
    '''
    cluster = Cluster('couchbase://10.99.143.96:8091')
    authenticator = PasswordAuthenticator('Administrator', 'password')
    cluster.authenticate(authenticator)
    cb = cluster.open_bucket('item')

    results = []

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

    if (len(results) == 0):
        return False
    else:
        return True