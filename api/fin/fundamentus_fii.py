#!/usr/bin/env python3

import re
import urllib.request
import urllib.parse
import http.cookiejar

from lxml.html import fragment_fromstring
from collections import OrderedDict
from decimal import Decimal

def get_data(*args, **kwargs):
    url = 'https://www.fundamentus.com.br/fii_resultado.php'
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca das fii
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min': '',
            'pl_max': '',
            'pvp_min': '',
            'pvp_max' : '',
            'psr_min': '',
            'psr_max': '',
            'divy_min': '',
            'divy_max': '',
            'pativos_min': '',
            'pativos_max': '',
            'pcapgiro_min': '',
            'pcapgiro_max': '',
            'pebit_min': '',
            'pebit_max': '',
            'fgrah_min': '',
            'fgrah_max': '',
            'firma_ebit_min': '',
            'firma_ebit_max': '',
            'margemebit_min': '',
            'margemebit_max': '',
            'margemliq_min': '',
            'margemliq_max': '',
            'liqcorr_min': '',
            'liqcorr_max': '',
            'roic_min': '',
            'roic_max': '',
            'roe_min': '',
            'roe_max': '',
            'liq_min': '',
            'liq_max': '',
            'patrim_min': '',
            'patrim_max': '',
            'divbruta_min': '',
            'divbruta_max': '',
            'tx_cresc_rec_min': '',
            'tx_cresc_rec_max': '',
            'setor': '',
            'negociada': 'ON',
            'ordem': '1',
            'x': '28',
            'y': '16'}

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="tabelaResultado".*</table>', re.DOTALL)
    content = re.findall(pattern, content)[0]
    page = fragment_fromstring(content)
    result = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        result.update({rows.getchildren()[0][0].getchildren()[0].text: {
                                                                        'Cotação': todecimal(rows.getchildren()[2].text),
                                                                        'FFO Yield': todecimal(rows.getchildren()[3].text),
                                                                        'Dividend Yield': todecimal(rows.getchildren()[4].text),
                                                                        'P/VP': todecimal(rows.getchildren()[5].text),
                                                                        'Valor de Mercado': todecimal(rows.getchildren()[6].text),
                                                                        'Liquidez': todecimal(rows.getchildren()[7].text),
                                                                        'Qtd de imóveis': todecimal(rows.getchildren()[8].text),
                                                                        'Preço do m2': todecimal(rows.getchildren()[9].text),
                                                                        'Aluguel por m2': todecimal(rows.getchildren()[10].text),
                                                                        'Cap Rate': todecimal(rows.getchildren()[11].text),
                                                                        'Vacância Média': todecimal(rows.getchildren()[12].text),
                                                                        }})
    
    return result
    
def todecimal(string):
  string = string.replace('.', '')
  string = string.replace(',', '.')

  if (string.endswith('%')):
    string = string[:-1]
    return float(string) / 100
  else:
    return float(string)


if __name__ == '__main__':
    from waitingbar import WaitingBar
    
    progress_bar = WaitingBar('[*] Downloading...')
    result = get_data()
    progress_bar.stop()

    result_format = '{0:<7} {1:<10} {2:<7} {3:<10} {4:<7} {5:<10} {6:<10} {7:<10} {8:<11} {9:<11} {10:<11} {11:<7}'
    print(result_format.format(
                              'Papel',
                              'Cotação',
                              'FFO Yield',
                              'Dividend Yield',
                              'P/VP',
                              'Valor de Mercado',
                              'Liquidez',
                              'Qtd de imóveis',
                              'Preço do m2',
                              'Aluguel por m2',
                              'Cap Rate',
                              'Vacância Média',
                               ))

    print('-' * 190)
    for key, value in result.items():
        print(result_format.format(
                                   key,
                                  value['Cotação'],
                                  value['FFO Yield'],
                                  value['Dividend Yield'],
                                  value['P/VP'],
                                  value['Valor de Mercado'],
                                  value['Liquidez'],
                                  value['Qtd de imóveis'],
                                  value['Preço do m2'],
                                  value['Aluguel por m2'],
                                  value['Cap Rate'],
                                  value['Vacância Média'],
                                   ))
