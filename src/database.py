import postgresql

class DB:
    def __init__(self):
        db = postgresql.open('pq://user:password@host:port/database')