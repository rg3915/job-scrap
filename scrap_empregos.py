from collections import namedtuple
from pprint import pprint
from bs4 import BeautifulSoup as bs
from requests import get

'''
www.empregos.com.br/
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
    boxes = vagas_page.find_all('div', {'class': 'descricao'})
    for box in boxes:
        titulo = box.find('h3').text
        empresa = box.find('span', {'class': 'nome-empresa'}).text
        publicado = box.find('span', {'class': 'publicado'}).text
        salario = box.find('span', {'class': 'valor-salario'}).text
        descricao = box.find('p', {'class': 'resumo-vaga'}).text
        yield vaga(
            remove_escape(titulo),
            remove_escape(empresa),
            remove_escape(publicado),
            remove_escape(salario),
            remove_escape(descricao)
        )


vaga = namedtuple('Vaga', 'Titulo Empresa Publicado Salario Descricao')
base_url = 'https://www.empregos.com.br/'
job = 'motorista'
jobs = '{}vagas/{}/'.format(base_url, job)
job_pages = '{}p'.format(jobs)
# last_page = get_last_page(jobs)
last_page = 2
urls = ['{}{}'.format(job_pages, n) for n in range(1, last_page + 1)]

for url in urls:
    pprint(list(get_jobs(url)))
