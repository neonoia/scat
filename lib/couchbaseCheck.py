from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery

class couchbaseCheck(object):

    def check_in_couchbase(self, sku):

        cluster = Cluster('couchbase://10.99.143.96:8091')
        authenticator = PasswordAuthenticator('Administrator', 'password')
        cluster.authenticate(authenticator)
        cb = cluster.open_bucket('item')

        results = []

        for sku_id in sku:
            query = N1QLQuery("SELECT code, name FROM `item` WHERE code=$codes", codes=str(sku_id))
            
            idx = 0
            for row in cb.n1ql_query(query):
                results.append(row)
                idx += 1

            if idx == 0:
                return False

        return True