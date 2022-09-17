import imob_properties_list as plist
import imob_property_details as pdetail
import imob_utils as iutil

usos = ['arrendar', 'comprar']
tipo_imoveis =['apartamento', 'moradia', 'quintaeherdade', 'predio']

# regions = {'aveiro':1, 'beja':2, 'braga':3, 'braganca':4, 'castelo-branco':5, 'coimbra':6,
#            'evora':7, 'faro':8, 'guarda':9, 'leiria':10, 'lisboa':11, 'portalegre':12, 
#            'porto':13, 'santarem':14, 'setubal':15, 'viana-do-castelo':16, 'vila-real':1,
#            'viseu':18}


#usos = ['comprar']
#tipo_imoveis = ['apartamento']
regions = {'lisboa':11, 'setubal':15}

site = 'Imovirtual'
num_carregamento = iutil.start_carregamento(site, usos, tipo_imoveis, regions)

for region in regions:
    for tipo_imovel in tipo_imoveis:
        for uso in usos:
            print('Start populating database (' + region +' | '+ tipo_imovel +' | '+ uso + ')...')
    
            pdetail.read_urls_file(uso, tipo_imovel, region, num_carregamento, site)
    
            print('Finish populating database (' + region +' | '+ tipo_imovel +' | '+ uso + ').')
            print()

iutil.stop_carregamento(num_carregamento)