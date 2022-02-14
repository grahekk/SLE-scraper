from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import collections
import pandas as pd

base_url = "https://sle.mps.hr"

driver = webdriver.Chrome()
driver.get(base_url)
time.sleep(0.1)

LOVISTEZAEXPORT = input("Ime lovista: ")

search_box = driver.find_element(By.TAG_NAME, "input.form-control.input-sm")
search_box.send_keys(LOVISTEZAEXPORT)

time.sleep(0.5)
loviste = driver.find_element(By.XPATH, '//*[@id="tblLovista"]/tbody/tr/td[2]/a')
loviste.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
podaci_loviste = soup.find_all("div",class_ = "form-group")
#ovo treba pospremiti

ugovor = driver.find_element(By.XPATH, '//*[@id="tblUgovori"]/tbody/tr/td[6]/a')
ugovor.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
podaci_ugovor = soup.find_all("div",class_ = "form-group")
#ovo treba isto pospremiti

pregled_lgpova = driver.find_element(By.XPATH, '//*[@id="tblUgovori"]/tbody/tr/td[4]/a')
pregled_lgpova.click()

lgo1_iskaz = driver.find_element(By.XPATH, '//*[@id="headingOne_1"]/h6/a')
lgo1_iskaz.click()
time.sleep(0.5)
lgo1 = driver.find_element(By.XPATH, '//*[@id="collapseOne_1"]/div/dd/a')
lgo1.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
table = soup.find_all
df = pd.read_html(str(table))[0]

df.to_excel((LOVISTEZAEXPORT + "_loviste_lgo1.xlsx"))

#tu krecem sa skrejpanjem podataka za divljac

i = 0
while i<4:
    i = i+1

    driver.back()
    lgo2_smjernice = driver.find_element(By.XPATH, '//*[@id="headingTwo_1"]/h4/a')
    lgo2_smjernice.click()
    time.sleep(0.5)

    divljacpath = '//*[@id="collapseTwo_1"]/div/dd['+str(i)+']/a'
    divljac = driver.find_element(By.XPATH, divljacpath)
    divljac.click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    podaci_divljac = soup.find_all("div", class_ = "form-group")
    dajmi = soup.find_all("label")

    #tekst za vrstu divljaci
    tekst = soup.get_text(",",strip = True)
    lista = tekst.split(",")
    lista = lista[17:47]

    lista1 = lista[::2]
    lista2 = lista[1::2]

    #dobivanje tablice za vrstu divljaci
    d = {'prvi stupac':lista1, 'drugi stupac': lista2}
    df = pd.DataFrame(d)
    df.to_excel((LOVISTEZAEXPORT + "_loviste_lgo2_"+lista[0]+".xlsx"))

driver.back()
print("gotof")

"""
for count,l in enumerate(lista[17:47]):
    print(count)
    print(l)
    if count%2==0:
        lista1 = lista1.append(l)
    else:
        lista2 = lista2.append(l)


i = 0
while i<12:
    i = i+1
    print(i)
    divljacpath = '//*[@id="collapseTwo_1"]/div/dd[' + str(i) + ']/a'
    print(divljacpath)
    try:
        divljac = driver.find_element(By.XPATH, divljacpath)
        divljac.click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        podaci_divljac = soup.find_all("div", class_="form-group")

    except:
        print("nema vise divljaci")

    driver.back()
    lgo2_smjernice.click()
    time.sleep(1)
    print(i)
"""

#f.close()
driver.close()