from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import BatchStatement



def create_connection():
    # Here fill in your own contact point
    cluster = Cluster(['34.65.83.35', '34.65.245.28', '34.65.214.229'])
    session = cluster.connect('airbnb')
    return session
