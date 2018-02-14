import json
from bs4 import BeautifulSoup as bs
from collections import namedtuple
from pprint import pprint
from requests import get
import ipdb
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
    vagas = get(url)
    vagas_page = bs(vagas.text, 'html.parser')
    boxes = vagas_page.find_all('div', {'class': 'element-vaga'})
    salario = []
    for a in vagas_page.find_all('a',{'class':'vagaTitle'}, href=True):
        link = (a['href'])
        vagas2 = get(link)
        vagas_page2 = bs(vagas2.content, 'html.parser')
        salario1 = vagas_page2.find('span', {'id': 'ctl00_phMasterPage_cVacancySummary_litSalary'})
        salario2 = salario1.get_text()
        salario.append(salario2)
    salariu = ''.join(salario)
    for box in boxes:
        titulo = box.find('div', {'class': 'vaga '}).text
        empresa = box.find('div', {'class': 'vaga-company'}).text
        publicado = box.find('span', {'class': 'data'}).text
        yield vaga(
            remove_escape(titulo),
            remove_escape(empresa),
            remove_escape(publicado),
            remove_escape(salariu)
        )

vaga = namedtuple('Vaga', 'Titulo Empresa Publicado Salario')
# vaga = namedtuple('Vaga', 'Titulo Empresa Publicado')
base_url = 'https://www.infojobs.com.br/'
job = 'motorista'
jobs = '{}vagas-de-emprego-{}.aspx?'.format(base_url, job)
job_pages = '{}Page='.format(jobs)
# last_page = get_last_page(jobs)
last_page = 2
urls = ['{}{}'.format(job_pages, n) for n in range(1, last_page + 1)]

for url in urls:
    print(list(get_jobs(url)))


with open('vagas.json', 'w') as f:
    for url in urls:
        json.dump(list(get_jobs(url)), f, indent=4,)