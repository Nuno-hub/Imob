# fuser imob_v01.db
# kill -9 <pid>

import sqlite3

class SQLData:
    ''' Manage SQLlite DB interactions.'''
    
    def __init__(self) -> None:
        self.__db = 'imob_v01.db'
        self.__table = 'imoveis'
       
    def connect(self):        
        self.__connection = sqlite3.connect(self.__db)
        return self.__connection
                
    def insert(self, conn, values:dict) -> None:
        print_on = False
        
        columns = ', '.join(values.keys())
        placeholders = ':'+', :'.join(values.keys())
        query = 'INSERT INTO ' + self.__table + ' (%s) VALUES (%s)' % (columns, placeholders)
        if print_on: print (query)
        if print_on: print (values)
        conn.execute(query, values)
        