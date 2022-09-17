from ssl import HAS_TLSv1
from turtle import clear
from SQLData import SQLData 
from bs4 import BeautifulSoup
import imob_utils as iutil
import traceback
import re
import ast
import datetime
import os

def load_property_details(url, log_file, sql, conn, num_carregamento, site, uso, tipo_imovel):
    '''Loads the informtion of each url into database.'''
    
    print_on = False

    # Initialize variables
    distrito = ''
    concelho = ''
    freguesia = ''
    titulo = ''
    preco = 0.0
    area_util = 0.0
    area_bruta = 0.0
    area_terreno = 0.0
    estado = ''
    tipologia = ''
    wc = ''
    cert_energetico = ''
    lic_utilizacao = ''
    data_ins_anuncio = ''
    data_alt_anuncio = ''
    descricao = ''
    ref_interna = ''
    id_anuncio = 0
    agencia = ''
    ano_construcao = 0
    
    # Get the page html.
    html = iutil.open_page(url, log_file)
    
    try:
        bs = BeautifulSoup(html, 'html.parser')  
        #log_file.write(str(bs))
        
        titulo = bs.find("title").text
        if print_on: print('Título: ', titulo)
        
        # Gets a string between start_str and end_str
        start_str = '\"characteristics\"\:'
        end_str = '\"images\"\:\['
        result = re.search('%s(.*)%s' % (start_str, end_str), str(bs)).group(1)
        if print_on: print('result: ', result)
        
        # Transforms the string in tuple
        data = ast.literal_eval(result)
        if print_on: print('type(data): ', type(data))
        
        len_data = int(len(data[0]))
        for i in range(len_data):
            if print_on: print(data[0][i])
            if data[0][i]['label']=='Preço':
                preco = data[0][i]['localizedValue']
                preco = preco.replace(' €', '').replace(' ','').replace(',', '.')
                preco = iutil.numeric_value(preco)
                if print_on: print('Preço: ', preco)
            elif data[0][i]['label']=='Área útil (m²)':
                area_util = data[0][i]['localizedValue']
                area_util = area_util.replace(' m²', '').replace(' ','').replace(',', '.')
                area_util = iutil.numeric_value(area_util)
                if print_on: print('Área útil (m²): ', area_util)
            elif data[0][i]['label']=='Área bruta (m²)':
                area_bruta = data[0][i]['localizedValue']
                area_bruta = area_bruta.replace(' m²', '').replace(' ','').replace(',', '.')
                area_bruta = iutil.numeric_value(area_bruta)
                if print_on: print('Área bruta (m²): ', area_bruta)    
            elif data[0][i]['label']=='Área de terreno (m²)':
                area_terreno = data[0][i]['localizedValue']
                area_terreno = area_terreno.replace(' m²', '').replace(' ','').replace(',', '.')
                area_terreno = iutil.numeric_value(area_terreno)
                if print_on: print('Área bruta (m²): ', area_bruta)                     
            elif data[0][i]['label']=='Condição':
                estado = data[0][i]['localizedValue']
                if print_on: print('estado: ', estado)
            elif data[0][i]['label']=='Tipologia':
                tipologia = data[0][i]['localizedValue']
                if print_on: print('tipologia: ', tipologia)
            elif data[0][i]['label']=='Ano de construção':
                ano_construcao = data[0][i]['localizedValue']
                if print_on: print('ano_construcao: ', ano_construcao)
            elif data[0][i]['label']=='Casas de Banho':
                wc = dict(data[0][i])['localizedValue']
                if print_on: print('wc: ', wc)    
            elif data[0][i]['label'] == 'Certificado Energético':
                cert_energetico = data[0][i]['localizedValue']
                if print_on: print('Cert Energetico: ', cert_energetico)               
            elif data[0][i]['label'] == 'nº de licença de utilização':
                lic_utilizacao = data[0][i]['localizedValue']
                if print_on: print('Licença de utilização: ', lic_utilizacao)  
            else:
                pass
        
        # Gets a string between start_str and end_str
        start_str = '\"advertiserType\"\:'
        end_str = '\"Photo\"\:'
        result = re.search('%s(.*)%s' % (start_str, end_str), str(bs)).group(1)
        
        # Not saving discription so no need to remove blanks, etc.
        #result = result.replace('\\u003cbr\/\\u003e\\r\\n', '')
        #result = result.replace('\\u003cp\\u003e', '')
        #result = result.replace('\\', '').replace('\/', '')
        
        # Creates a list with items corresponding to strings between quotation marks
        data = re.findall('"([^"]*)"', result)
        if print_on: print('data: ', data)

        len_data = int(len(data))
        for i in range(len_data):
            if print_on: print(data[i])
            if data[i]=='dateCreated':
                data_ins_anuncio = data[i+1]
                if print_on: print('Data de criação do anúncio: ', data_ins_anuncio)
            elif data[i]=='dateModified':
                data_alt_anuncio = data[i+1]
                if print_on: print('Data de atualização do anúncio: ', data_alt_anuncio)
            #elif data[i]=='description':
            #    descricao = data[i+1]
            #    if print_on: print('Descrição: ', descricao)
            elif data[i]=='referenceId':
                ref_interna = data[i+1]
                if print_on: print('Referência interna: ', ref_interna)
            elif data[i]=='Id':
                id_anuncio = data[i+1]
                if print_on: print('Id do anúncio: ', id_anuncio)
            else:
                pass

        try:
            # Gets a string between start_str and end_str
            start_str = '\"agency\"\:\{\"id\"\:'
            end_str = '\"licenseNumber\"\:'
            result = re.search('%s(.*)%s' % (start_str, end_str), str(bs)).group(1)
            if print_on: print('result: ', result)
            
            # Creates a list with items corresponding to strings between quotation marks
            data = re.findall('"([^"]*)"', result)
            if print_on: print('data: ', data)
            
            len_data = int(len(data))
            for i in range(len_data):
                if print_on: print(data[i])
                if data[i]=='name':
                    agencia = data[i+1]
                    if print_on: print('Agência: ', agencia) 
        except:
            agencia = ''
                
        # Gets a string between start_str and end_str
        #start_str = '\"geoLevels\"\:\[\{'
        #end_str = '\:\"AdvertGeoLevel\"\}\]'
        # 2022-08-06 change in site structure
        start_str = '\"itemListElement\"\:\['
        end_str = '\}\}\]\}\<\/script\>'
        result_region = re.search('%s(.*)%s' % (start_str, end_str), str(bs)).group(1)
        if print_on: print('result: ', result)
        
        # Distrito
        start_str = '\"position\"\:2'
        end_str = '\}\}'
        result = re.search('%s(.*)%s' % (start_str, end_str), result_region).group(1)
         # Creates a list with items corresponding to strings between quotation marks
        data = re.findall('"([^"]*)"', result)
        if print_on: print('data: ', data)
        len_data = int(len(data))
        for i in range(len_data):
            if print_on: print(data[i])
            if data[i]=='name':     
                distrito = data[i+1].replace('(distrito)', '')  
                distrito = distrito.rstrip()
                #print('distrito: ', distrito)
                break
        
        # Concelho
        start_str = '\"position\"\:3'
        end_str = '\}\}'
        result = re.search('%s(.*)%s' % (start_str, end_str), result_region).group(1)
         # Creates a list with items corresponding to strings between quotation marks
        data = re.findall('"([^"]*)"', result)
        if print_on: print('data: ', data)
        
        len_data = int(len(data))
        for i in range(len_data):
            if print_on: print(data[i])
            if data[i]=='name':     
                concelho = data[i+1].replace('(concelho)', '') 
                concelho = concelho.rstrip()
                break
        
        # Freguesia
        start_str = '\"position\"\:4'
        end_str = '\}\}'
        result = re.search('%s(.*)%s' % (start_str, end_str), result_region).group(1)
         # Creates a list with items corresponding to strings between quotation marks
        data = re.findall('"([^"]*)"', result)
        if print_on: print('data: ', data)
        len_data = int(len(data))
        for i in range(len_data):
            if print_on: print(data[i])
            if data[i]=='name':     
                freguesia = data[i+1] 
                break    
        
        # 2022-08-16 change in site structure      
        # len_data = int(len(data))
        # for i in range(len_data):
        #     if print_on: print(data[i])
        #     if data[i]=='label' and data[i+3]=='region':
        #         distrito = data[i+1]
        #         if print_on: print('Distrito: ', distrito)
        #     if data[i]=='label' and data[i+3]=='sub-region':
        #         concelho = data[i+1]
        #         if print_on: print('Concelho: ', concelho)
        #     if data[i]=='label' and data[i+3]=='city':
        #         freguesia = data[i+1]
        #         if print_on: print('Freguesia: ', freguesia)
        #     else:
        #         pass

        values = {
            'num_carregamento': num_carregamento,
            'uso': uso,
            'url': url,
            'distrito': distrito,
            'concelho': concelho,
            'freguesia': freguesia,
            'titulo': titulo,
            'preco': preco,
            'area_util': area_util,
            'area_bruta': area_bruta,
            'estado': estado,
            'tipologia': tipologia,
            'wc': wc,
            'cert_energetico': cert_energetico,
            'lic_utilizacao': lic_utilizacao,
            'data_ins_anuncio': data_ins_anuncio,
            'data_alt_anuncio': data_alt_anuncio,
            'descricao': descricao,
            'ref_interna': ref_interna,
            'id_anuncio': id_anuncio, 
            'data_carregamento_bd': str(datetime.now()),
            'site': site,
            'agencia': agencia,
            'ano_construcao': ano_construcao,
            'tipo_imovel': tipo_imovel,
            'area_terreno': area_terreno
            }
        
        print('Zona: ', distrito + ' > ' + concelho + ' > ' + freguesia)
        sql.insert(conn, values)
        return True
        
    except:
        e = traceback.format_exc()
        iutil.write2log_file(log_file, e, url, '', '')
        print('url:   ', url)
        print('e: ', e)
        return False


def read_urls_file(uso, tipo_imovel, region, num_carregamento, site):
    '''Iterates over the file with the url list to read the web pages as populate the database.'''
    #print('start!')
    
    #url = 'https://www.imovirtual.com/pt/anuncio/alugo-apartamento-t2-com-80m2-bobadela-ID17faI.html#555d8542cc'
    #url = 'https://www.imovirtual.com/pt/anuncio/apartamento-em-sintra-queluz-ID197If.html#555d8542cc'
    #url = 'https://www.imovirtual.com/pt/anuncio/apartamento-t3-com-garagem-para-arrendar-sem-moveis-na-lapa-lisboa-ID19bvc.html#727b013a00'
    
    try:
        
        # Errors log file
        log_file = iutil.error_log_file()
        
        sql = SQLData()
        conn = sql.connect()
        cursor = conn.cursor()
        
        #buy_or_rent = uso   # 'arrendar' | 'comprar'
        #region = 'lisboa'
        filename = 'properties_list_' + region +'_'+ tipo_imovel + '_' + uso + '.txt'
        file = open(os.getcwd() + '/data/' + filename, 'r')
        lines = file.readlines()
        cont = 0
        cont_error = 0
        # Gather the information of each url in the file name
        for line in lines:
            url = line
            result = load_property_details(url, log_file, sql, conn, num_carregamento, site, uso, tipo_imovel)
            if result:
                cont += 1
            else:
                cont_error += 1
            # Commit's every 10 inserts
            if (cont%10) == 0:
                conn.commit()
                print('Number of inserted records ('+region+'_'+tipo_imovel+'_'+uso+'): ', cont)
    except:
        url_next = ""
        e = traceback.format_exc()
        iutil.write2log_file(log_file, e, url, 0, '')
        print(e)

    finally:  
        print('URL`s com erro: ', str(cont_error))
        iutil.write2log_file(log_file, '', 'URL`s com erro: ' + str(cont_error), 0, '')
        
        file.close()

        conn.commit()
        cursor.close()
        conn.close()

        log_file.close()


if __name__ == '__main__':
    read_urls_file()
