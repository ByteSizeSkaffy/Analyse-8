import sqlite3
import hashlib
def hashPW(password):
    return hashlib.sha3_256(password.encode()).hexdigest()

