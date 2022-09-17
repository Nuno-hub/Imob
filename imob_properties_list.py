import imob_utils as iutil
from bs4 import BeautifulSoup
import traceback
import os

def properties_list_file(name):
    '''Create a file with a list of properties links.'''
    return open(os.getcwd() +'/data/'+ name, "w")

def extract_links_in_page(html, file, error_log_file, cont):
    '''Get the url of all advertises in the page'''

    try:
        bs = BeautifulSoup(html, 'html.parser')
        
        property_link = ''
        # Get the properties advertises url of the page.
        for properties in bs.find_all("article"):
            cont += 1
            
            property_link = properties.get("data-url")           
            #print(property_link)
            
            # writes to file each property link.
            file.write(property_link + "\n")
                
            if (cont%100) == 0:
                print('Number of url`s extracted: ', cont)            
                
        # Get next page url.          
        pag_next = bs.find("li", {"class": "pager-next"})
        url_next = pag_next.a['href']
        #print('url_next = ', url_next)
    except:
        url_next = ""
        e = traceback.format_exc()
        iutil.write2log_file(error_log_file, e, property_link, cont, url_next)
        
        # print("Trace do erro: ", e)
        # print("property_link: ", property_link)
        # print('url_next = ', url_next)
        # print()

    return url_next, cont

def create_properties_list_file(uso, tipo_imovel, region, region_id):
       
    # Properties file
    filename = 'properties_list_' + region +'_'+ tipo_imovel + '_' + uso + '.txt'
    file = properties_list_file(filename)
    
    # Errors log file
    log_file = iutil.error_log_file()
    
    str_description = uso + '/' + tipo_imovel + '/' + region
    region_id = '/?search%5Bdescription%5D=1&search%5Bregion_id%5D=' + str(region_id) 
    ads_per_page = '/&nrAdsPerPage=72'
    initial_url = 'https://www.imovirtual.com/' + str_description + region_id + ads_per_page
    # print('initial_url: ', initial_url)

    cont = 0
    url_next = initial_url
    while url_next != "":    
        # Get the page html.
        html = iutil.open_page(url_next, log_file)
        # Extracts the properties links in the html.
        url_next, cont = extract_links_in_page(html, file, log_file, cont)
    
    log_file.close()
    file.close()

if __name__ == '__main__':
    #print('start!')
    create_properties_list_file()
 
  
    # titulo = 'teste'
    # values = {'titulo':titulo}
    
    # db = 'imob_v01.db'
    # table = 'imoveis'
    # sql = SQLData(db)
    # sql.connect()
    # sql.cursor()
    # sql.insert(table, values)
    # sql.commit()
    # sql.cur_close()
    # sql.conn_close()
 