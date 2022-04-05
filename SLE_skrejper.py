from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd

start = time.time()
base_url = "https://sle.mps.hr"
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
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


#saving the metadata for hunting grounds
podaci_loviste = soup.find_all("div",class_ = "form-group")
podaci_loviste_label = []
for lab in soup.find_all(name = "label"):
    podaci_loviste_label.append(lab.text)

#i'm still missing the "tip reljefa info"

podaci_loviste_label_drugi = []
for lab in podaci_loviste:
    string2 = lab.text.split("\n")
    string2 = (list(filter(None,string2)))
    string2 = [name for name in string2 if name.strip()]
    string2 = [s.replace("                                ","") for s in string2]
    if len(string2)>2:
        string2[1:] = ["".join(string2[1:])]
    podaci_loviste_label_drugi.append(string2)

df = pd.DataFrame(podaci_loviste_label_drugi).transpose()
df.columns = df.iloc[0]
df = df[1:]
#df.to_excel((LOVISTEZAEXPORT + "_podaci o lovistu.xlsx"))
tablica = df


ugovor = driver.find_element(By.XPATH, '//*[@id="tblUgovori"]/tbody/tr/td[6]/a')
ugovor.click()

#contract data
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
podaci_ugovor = soup.find_all("div",class_ = "form-group")
podaci_ugovor_label = []
for lab in podaci_ugovor:
    string2 = lab.text.split("\n")
    string2 = (list(filter(None,string2)))
    string2 = [name for name in string2 if name.strip()]
    string2 = [s.replace("                                ","") for s in string2]
    string2 = [s.replace("                            ","") for s in string2]
    if len(string2)>2:
        string2[1:] = ["".join(string2[1:])]
    podaci_ugovor_label.append(string2)

podaci_ugovor_label=podaci_ugovor_label[1:]
df = pd.DataFrame(podaci_ugovor_label).transpose()
df.columns = df.iloc[0]
df = df[1:]
tablica = pd.concat([tablica,df], axis=1)

#df.to_excel((LOVISTEZAEXPORT + "_podaci o ugovoru.xlsx"))

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
broj_divljaci = int(re.findall(r'\d',lgo2_smjernice.text)[1])
lgo2_smjernice.click()
time.sleep(1)

#scraping the main game data from LGO2 to table
lgo2_divljac = []
i = 0
while i < broj_divljaci:
    i = i+1
    divljacpath = '//*[@id="collapseTwo_1"]/div/dd['+str(i)+']/a'
    divljac = driver.find_element(By.XPATH, divljacpath)
    divljac.click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    podaci_divljac = soup.find_all("div", class_ = "form-group")

    ime_divljaci = driver.find_element(By.XPATH, '/html/body/section/div/div[2]/div/div/div[2]/div[1]/div[1]/h4/span').text
    podaci_divljac_label = []
    for lab in podaci_divljac:
        string2 = lab.text.split("\n")
        string2 = (list(filter(None, string2)))
        string2 = [name for name in string2 if name.strip()]
        string2 = [s.replace("                                ", "") for s in string2]
        string2 = [s.replace("              ", "") for s in string2]
        if len(string2) > 2:
            string2[1:] = ["".join(string2[1:])]
        if "Dobna struktura" in string2:
            continue
        string2 = [ime_divljaci + " - " + s for s in string2]
        podaci_divljac_label.append(string2)
    lgo2_divljac.append(podaci_divljac_label)

    df = pd.DataFrame(podaci_divljac_label).transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    tablica = pd.concat([tablica, df], axis=1)

    #for lab in soup.find_all(name="label"):
        #podaci_loviste_label.append(lab.text)

    #dobivanje tablice za vrstu divljaci
    #d = {'prvi stupac':lista1, 'drugi stupac': lista2}
    #df = pd.DataFrame(d)
    #df.to_excel((LOVISTEZAEXPORT + "_loviste_lgo2_"+lista2[0]+".xlsx"))

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

tablica['sitna_divljac'] = ', '.join(map(str, sitna_divljac))

#table of technical objects on hunting ground

lgo11_objekti = driver.find_element(By.XPATH, '//*[@id="headingFive_1"]/h4/a')
lgo11_objekti.click()
time.sleep(0.5)
lgo11_objekti = driver.find_element(By.XPATH, '//*[@id="collapseFive_1"]/div/dd/a')
lgo11_objekti.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
table = soup.find_all
df = pd.read_html(str(table))[0]

df.columns = ["VRSTA OBJEKTA", "REDNI BROJ OBJEKTA", "LOKACIJA", "Z. ŠIRINA (φ)", "Z. DUŽINA (λ)"]
df = df['VRSTA OBJEKTA'].value_counts().to_frame().transpose().rename(index={"VRSTA OBJEKTA":1})
tablica = pd.concat([tablica, df], axis=1)

tablica.to_excel("Loviste_redak_gotov.xlsx")

driver.back()
print(time.time() - start)
driver.close()