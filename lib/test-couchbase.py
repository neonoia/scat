from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery

cluster = Cluster('couchbase://10.99.143.96:8091')
authenticator = PasswordAuthenticator('Administrator', 'password')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('item')

query = N1QLQuery("SELECT name, size, created_at FROM `item` WHERE code=$codes", codes="PRTA12346")

for row in cb.n1ql_query(query):
    print(row)