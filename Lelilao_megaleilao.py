# -*- encoding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import re
from pprint import pprint
import string
import numpy as np

i = 1
# Grab content from URL (Pegar conteúdo HTML a partir da URL)
url = "https://www.megaleiloes.com.br/imoveis/apartamentos/sp?tov=igbr&valor_max=500000&tipo[0]=1&tipo[1]=2&pagina=" 
#Xpath da texto com local da paginação
ClassXpathPagina = "summary"
ClassXpathcapturaHTML = "page"
ClassXpathClasseLeilao = "col-sm-6 col-md-4 col-lg-3"


def Paginador():
    pagina = driver.find_element_by_xpath("//div[@class='" + ClassXpathPagina +"' ]")
    pagina_content = pagina.get_attribute('outerHTML')
    souppagina = BeautifulSoup(pagina_content, 'html.parser')
    paginacao = souppagina.find_all("div", attrs={"class": "" + ClassXpathPagina + ""})
    return paginacao
    #print(paginacao1)


option = Options()
option.headless = True
driver = webdriver.Firefox(executable_path=r"C:\Users\carlo\AppData\Local\Programs\Python\Python39\Scripts\geckodriver.exe")
driver.get(url + str(i))
driver.implicitly_wait(5)  # in seconds
#driver.find_element_by_class_name("fancybox-close").click();





#print (driver.current_url)
paginacao1 = Paginador()
#paginacao1 = (driver.current_url)

#print(paginacao1)

Lista_leilao = []
while i > 0:
    i += 1
    #recupera o numero da paginação para comparar e saber se chegou ai final dos registros
    #print (driver.current_url)
    paginacao1 = Paginador()
    #paginacao1 = driver.current_url
    #recupera o hmtl com dados da pagina dos leilos
    element = driver.find_element_by_xpath("//div[@class='" + ClassXpathcapturaHTML +"']")
    html_content = element.get_attribute('outerHTML')
    # Parse HTML (Parsear o conteúdo HTML) - BeaultifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    #encontra o inicio do loop dos leiloes
    a = 0
    for leilao in soup.find_all("div", attrs={"class": "" + ClassXpathClasseLeilao + ""}):
        dados_leilao = []
        resultado_busca_nome = re.findall(r'(.*?)-', leilao.find("a", attrs={"class": "card-title"}).text, flags=re.IGNORECASE)
        tipo = re.findall(r'(.*\D)\d+\D+',resultado_busca_nome[0])
        dados_leilao.append(re.findall(r'(.*\D)\d+\D+',resultado_busca_nome[0])) #tipo
        #print(leilao.find("a", attrs={"class": "card-title"}).text) #tipo
        dados_leilao.append(re.findall(r'\d+',resultado_busca_nome[0])) #metragem
        dados_leilao.append(resultado_busca_nome[1]) #bairro
        if leilao.find("div", attrs={"card-down"}) is None:
            desconto = "" #Desconto
        else:
            desconto = str(re.findall(r'\d{2}%',leilao.find("div", attrs={"card-down"}).text)) #Desconto
        dados_leilao.append(desconto) #Desconto
        dados_leilao.append("") #Rua
        cidade = re.findall(r'(.*),',leilao.find("a", attrs={"card-locality"}).text)
        dados_leilao.append(cidade) #Cidade
        estado = re.findall(r',(.*)',leilao.find("a", attrs={"card-locality"}).text)
        dados_leilao.append(str(estado)) #estado
            
        if leilao.find("div", attrs={"class": "instance first active"}) is None :
            praca1 = leilao.find("div", attrs={"class": "instance first passed"}) 
        else :
            praca1 = leilao.find("div", attrs={"class": "instance first active"})

        if praca1 is None :
            praca1=""    
        else:
            praca1 = re.findall(r'R\$.*', praca1.text)
        dados_leilao.append(praca1) #1o leilao
        praca2 = re.findall(r'R\$.*', leilao.find("div", attrs={"class": "instance active"}).text)
        dados_leilao.append(praca2) #2o leilao
        Datapraca2 = re.findall(r'\d{2}\/\d{2}\/\d{4}', leilao.find("div", attrs={"class": "instance active"}).text) #data2leilao
        dados_leilao.append(Datapraca2) #data2leilao
        linka = leilao.find("a", attrs={"class": "card-title"})['href'] #link
        dados_leilao.append(linka) #link
        Lista_leilao.append(dados_leilao) 
        #print(Lista_leilao)
        # a += 1
        # print (a)
    
    
    driver.get(url + str(i))
    #driver.find_element_by_class_name("next").click()
   # if driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div[2]/ul/li[6]/a/span").
    #    print (driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div[2]/ul/li[6]/a/span"))
     #   driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div[2]/ul/li[6]/a/span").click()

    driver.implicitly_wait(15)  # in seconds

    #print (driver.current_url)
    
    #paginacao2 = driver.current_url
    paginacao2 = Paginador()
    print (paginacao1)
    print (paginacao2)
    
    if paginacao1 == paginacao2:
        i=0
    print (i)


leilao_df = pd.DataFrame(Lista_leilao, columns=['tipo','metragem','Bairo', 'Desconto', 'Rua','cidade','estado','lance 1','lance 2','data 2a praca','link'])
new_leilao = leilao_df.replace("[","")
print(new_leilao)
leilao_df .to_csv('leilaomega.csv', index=False)
driver.quit()



# Dump and Save to JSON file (Converter e salvar em um arquivo JSON)
#with open('ranking.json', 'w', encoding='utf-8') as jp:
#    js = json.dumps(top10ranking, indent=4)
#    jp.write(js)