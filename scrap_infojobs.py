from collections import namedtuple
from pprint import pprint
from bs4 import BeautifulSoup as bs
from requests import get
import json

'''
www.infojobs.com.br/
'''

def get_last_page(url):
    '''
    Retorna a última página
    :param url: link da página
    :return int: Número da última página
    '''
    vagas = get(url)
    vagas_page = bs(vagas.text, 'html.parser')
    links = vagas_page.find('div', {'class': 'pagination-result'})
    links = links.text.strip().split()
    links = links[-1]
    return int(links)

def remove_escape(s):
    '''
    Remove \n \t \r
    :param s: texto
    :return str: texto limpo
    '''
    return ' '.join(s.split())

def get_jobs(url):
    '''
    Retorna um iterável com as vagas da página.
    :param url: link da página
    :return namedtuple: 'Vaga'
    '''
    lista = []
    vagas = get(url)
    vagas_page = bs(vagas.text, 'html.parser')
    boxes = vagas_page.find(id="ctl00_phMasterPage_cGrid_divGrid")

    nome_vagas = boxes.find_all(class_="vaga ")
    nome_empresas = boxes.find_all(class_="vaga-company")
    data = boxes.find_all(class_="data")
    
    prvagas = []
    prempresas = []
    prdias = []

    for vagas in nome_vagas:
        vagas2 = vagas.get_text().strip()
        prvagas.append(vagas2)

    for empresas in nome_empresas:
        empresas2 = empresas.get_text().strip()
        prempresas.append(empresas2)

    for dia in data:
        dias = dia.get_text().strip()
        prdias.append(dias)

    for i in zip(prvagas, prempresas, prdias):
        dt = {}
        dt['vaga'] = i[0]
        dt['empresa'] = i[1]
        dt['data'] = i[2]
        lista.append(dt)
        
    return(lista)
    
#vaga = namedtuple('Vaga', 'Titulo Empresa Publicado')
base_url = 'https://www.infojobs.com.br/'
job = 'motorista'
jobs = '{}vagas-de-emprego-{}.aspx?'.format(base_url, job)
job_pages = '{}Page='.format(jobs)
# last_page = get_last_page(jobs)
last_page = 2
urls = ['{}{}'.format(job_pages, n) for n in range(1, last_page + 1)]

for url in urls:
    print(list(get_jobs(url)))
'''
with io.open('vagas.json', 'w') as f:
    json.dump(get_jobs, f, indent=4,)
'''