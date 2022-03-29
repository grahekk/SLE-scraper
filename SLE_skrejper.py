from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd

base_url = "https://sle.mps.hr"

driver = webdriver.Chrome()
driver.get(base_url)
time.sleep(0.1)

LOVISTEZAEXPORT = input("Ime lovista: ")

search_box = driver.find_element(By.TAG_NAME, "input.form-control.input-sm")
search_box.send_keys(LOVISTEZAEXPORT)

time.sleep(1)
loviste = driver.find_element(By.XPATH, '//*[@id="tblLovista"]/tbody/tr/td[2]/a')
loviste.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
podaci_loviste = soup.find_all("div",class_ = "form-group")
#ovo treba pospremiti

#pospremanje
podaci_loviste_label = []
for lab in soup.find_all(name = "label"):
    podaci_loviste_label.append(lab.text)

for c,lab in enumerate(podaci_loviste):
    string2 = lab.text
    string2 = string2.split("\n")
    string2 = [item for item in string2 if item not in podaci_loviste_label]
    string2 = (list(filter(None,string2)))
    string2 = [name for name in string2 if name.strip()]
    string2 = [s.replace("                                ","") for s in string2]
    print(string2)
#sad treba spojiti te dvije liste u tablicu

ugovor = driver.find_element(By.XPATH, '//*[@id="tblUgovori"]/tbody/tr/td[6]/a')
ugovor.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
podaci_ugovor = soup.find_all("div",class_ = "form-group")
#ovo treba isto pospremiti
print("PODACI UGOVOR")
print(podaci_ugovor)


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

#clicking on the second falling list
driver.back()
lgo2_smjernice = driver.find_element(By.XPATH, '//*[@id="headingTwo_1"]/h4/a')
#the number of iterations or the number of the game species
broj_divljaci = int(re.findall('\d',lgo2_smjernice.text)[1])
lgo2_smjernice.click()
time.sleep(1)

#scraping the main game data from LGO2 to table
i = 0
while i < broj_divljaci:
    i = i+1
    divljacpath = '//*[@id="collapseTwo_1"]/div/dd['+str(i)+']/a'
    divljac = driver.find_element(By.XPATH, divljacpath)
    divljac.click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    podaci_divljac = soup.find_all("div", class_ = "form-group")

    #tekst za vrstu divljaci
    tekst = soup.get_text(",",strip = True)
    lista = tekst.split(",")
    lista = lista[17:47]
    lista1 = lista[::2]
    lista2 = lista[1::2]

    #dobivanje tablice za vrstu divljaci
    d = {'prvi stupac':lista1, 'drugi stupac': lista2}
    df = pd.DataFrame(d)
    df.to_excel((LOVISTEZAEXPORT + "_loviste_lgo2_"+lista2[0]+".xlsx"))

    driver.back()
    lgo2_smjernice = driver.find_element(By.XPATH, '//*[@id="headingTwo_1"]/h4/a')
    time.sleep(1)
    lgo2_smjernice.click()
    time.sleep(1)

lgo7b_smjernice = driver.find_element(By.XPATH, '//*[@id="headingFour_1"]/h4/a')
lgo7b_smjernice.click()
#again, the number of species of the small game
broj_divljaci = int("".join(map(str, re.findall(r"\(([^)]*)\)[^(]*$", lgo7b_smjernice.text))))

#list of small game species
i=0
sitna_divljac = []
while i < broj_divljaci:
    i=i+1
    divljacpath = '//*[@id="collapseFour_1"]/div/dd['+str(i)+']/a'
    divljac = driver.find_element(By.XPATH, divljacpath)
    sitna_divljac.append(divljac.text.split(" / ")[1])
    #ovo pospremiti

#table of technical objects on hunting ground


driver.back()
print("gotof")
driver.close()