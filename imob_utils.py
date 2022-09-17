from urllib.request import Request, urlopen
from datetime import datetime
import traceback
from xmlrpc.client import boolean
from SQLData import SQLData
import os

def error_log_file():
    '''Create a log file with timestamp in the name.'''
    x = str(datetime.datetime.now())
    x = x.replace(".", "_")
    x = x.replace(":", "_")
    x = x.replace(" ", "_")
    x = os.getcwd() + "/log/imobLog" + "_" + x + ".txt"
    return open(x, "a")

def open_file(filename):
    '''Open a file for reading.'''
    return open(os.getcwd() +'/data/'+ filename, 'r')
    
def open_page(url, error_log_file):
    '''Open the main url to extract the links for each item.'''

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    flag = False
    while not flag:
        try:
            html = urlopen(req).read()
            flag = True
        except:
            e = traceback.format_exc()
            # print(">------------------------- open_page(url) --------------------------------------")
            # print(str(datetime.datetime.now()))
            # print("url:", url)
            # print("Error trace: ", e)
            # print("-------------------------- open_page(url) -------------------------------------<")
            error_log_file.write(">------------------------- open_page(url) --------------------------------------" + "\n")
            error_log_file.write(str(datetime.datetime.now()))
            error_log_file.write("url: " + url + "\n")
            error_log_file.write("Error trace: " + e + "\n")
            error_log_file.write("-------------------------- open_page(url) -------------------------------------<" + "\n")
            flag = False
              
    return html


# def id_carregamento(site: str)->int:
#     sql = SQLData()
#     conn = sql.connect()
#     cursor = conn.cursor()
    
#     sql_Query = "select max(num_carregamento) valor from imoveis where site=:site"
    
#     input = {'site':site}  
#     cursor.execute(sql_Query, input)
#     record = cursor.fetchone()
#     if record[0] is None:
#         val = 0
#     else:
#         val = record[0]
#     print('id_carregamento: ', val + 1)
    
#     cursor.close()
#     conn.close()
#     return val + 1


def start_carregamento(siteimob: str, 
                       usos: list,
                       tipo_imoveis: list, 
                       regions: list)->int:
    
    sql = SQLData()
    conn = sql.connect()
    cursor = conn.cursor()
    
    sql_Query = "select max(num_carregamento) valor from loadcontrol"
    cursor.execute(sql_Query)
    record = cursor.fetchone()
    if record[0] is None:
        val = 0
    else:
        val = record[0]
    
    cursor.close()
    
    num_carregamento = int(val) + 1
    print('num_carregamento: ', num_carregamento)
    
    
    datetime_start = datetime.now()
    datetime_start = datetime_start.strftime("%Y-%m-%d, %H:%M:%S")
    datetime_stop = None
    details = '[' + ' '.join(usos) + '] ' + \
              '[' + ' '.join(tipo_imoveis)  + '] ' + \
              '[' + ' '.join(regions) + ']'
    
    sql_Insert = "insert into loadcontrol(num_carregamento, \
                datetime_start, datetime_stop, siteimob,\
                details) values \
                (:num_carregamento, :datetime_start, :datetime_stop, \
                :siteimob, :details)"
    
    input = {'num_carregamento':num_carregamento,
             'datetime_start':datetime_start,
             'datetime_stop':datetime_stop,
             'siteimob':siteimob, 
             'details':details}
                 
    cursor = conn.cursor()
    cursor.execute(sql_Insert, input)
    conn.commit()
    cursor.close()
    
    conn.close()
    
    return num_carregamento
   
    
def stop_carregamento(num_carregamento: int):
    
    sql = SQLData()
    conn = sql.connect()
    cursor = conn.cursor()
    
    datetime_stop = datetime.now()
    datetime_stop = datetime_stop.strftime("%Y-%m-%d, %H:%M:%S")
    
    sql_Update = "update loadcontrol set datetime_stop=:datetime_stop \
                  where num_carregamento=:num_carregamento"
    
    cursor = conn.cursor()
    input = {'datetime_stop':datetime_stop, 'num_carregamento':num_carregamento}
    cursor.execute(sql_Update, input)
    conn.commit()
    cursor.close()
    
    conn.close()   
    
    
def write2log_file(error_log_file, e, href, pag, url_next):
        error_log_file.write(">--------------------------------------------------------------------------------------------" + "\n")
        error_log_file.write(str(datetime.datetime.now())+ "\n")
        error_log_file.write("href: " + href + "\n")
        if pag!=0: error_log_file.write("pag: " + str(pag) + "\n")
        if pag!='': error_log_file.write("url_next: " + url_next + "\n")
        error_log_file.write("ERROR TRACE: " + e + "\n")
        error_log_file.write("\n")
        
def numeric_value(var: str):
    try:
        val = float(var)
    except:
        val = 0
    return val