from pygal.maps.world import COUNTRIES
from pygal.maps.world import World
from pygal.style import RotateStyle
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# częsć nazw krajów w danych nie eodpowiada nazwom w COUNTRIES
mapping_of_bad_names = {
    'Russia': 'Russian Federation',
    'Vietnam': 'Viet Nam',
    'DR Congo': 'Congo, the Democratic Republic of the',
    'Iran': 'Iran, Islamic Republic of',
    'Tanzania': 'Tanzania, United Republic of',
    'South Korea': 'Korea, Republic of',
    'Venezuela': 'Venezuela, Bolivarian Republic of',
    "Côte d'Ivoire": "Cote d'Ivoire",
    'North Korea': "Korea, Democratic People's Republic of",
    'Taiwan': 'Taiwan, Province of China',
    'Syria': 'Syrian Arab Republic',
    'Bolivia': 'Bolivia, Plurinational State of',
    'South Sudan': 'Sudan',
    'Czech Republic (Czechia)': 'Czech Republic',
    'Laos': "Lao People's Democratic Republic",
    'Libya': 'Libyan Arab Jamahiriya',
    'State of Palestine': 'Palestine, State of',
    'Moldova': 'Moldova, Republic of',
    'North Macedonia': 'Macedonia, the former Yugoslav Republic of',
    'Trinidad and Tobago': 'Trinidad and Tobago',
    'Eswatini': 'Swaziland',
    'Micronesia': 'Micronesia, Federated States of',
    'Brunei': 'Brunei Darussalam',
    'Sao Tome & Principe': 'Sao Tome and Principe',
    'St. Vincent & Grenadines': 'Saint Vincent and the Grenadines',
    'U.S. Virgin Islands': 'Virgin Islands, U.S.',
    'Marshall Islands': 'Marshall Islands',
    'Northern Mariana Islands': 'Northern Mariana Islands',
    'American Samoa': 'American Samoa',
    'Saint Kitts & Nevis': 'Saint Kitts and Nevis',
    'Faeroe Islands': 'Faroe Islands',
    'Sint Maarten': 'Sint Maarten (Dutch part)',
    'Turks and Caicos': 'Turks and Caicos Islands',
    'Saint Martin': 'Saint Martin (French part)',
    'British Virgin Islands': 'Virgin Islands, British',
    'Caribbean Netherlands': 'Bonaire, Sint Eustatius and Saba',
    'Wallis & Futuna': 'Wallis and Futuna',
    'Saint Barthelemy': 'Saint Barthélemy',
    'Saint Helena': 'Saint Helena, Ascension and Tristan da Cunha',
    'Saint Pierre & Miquelon': 'Saint Pierre and Miquelon',
    'Falkland Islands': 'Falkland Islands (Malvinas)',
    'Holy See': 'Holy See (Vatican City State)',
    }
    
def corecting_country_names(country):
    """ funkcja naprawia nazwy krajów, aby poprawnie tłumaczono je na kod kraju"""
    if country in mapping_of_bad_names.keys():
        return mapping_of_bad_names[country]
    else: 
        return country
    
def scrap_country_table(filename):
    """ funkcja pobiera dane ze strony worldmeter na temat ilo
    # Konfiguracja przeglądarki Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # Inicjalizacja sterownika Chrome
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    
    # Wizyta na stronie
    url = 'https://www.worldometers.info/world-population/population-by-country/'
    browser.get(url)
    
    # Czekanie na załadowanie się tabeli
    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//table[@id='example2']")))
    
    # Pobieranie nagłówków tabeli
    header = [h.text for h in browser.find_elements_by_xpath("//table[@id='example2']//thead/tr/th")]
    
    # Pobieranie danych z tabeli
    table_data = []
    rows = browser.find_elements_by_xpath("//table[@id='example2']//tbody/tr")
    for row in rows:
        row_data = [data.text for data in row.find_elements_by_xpath(".//td")]
        table_data.append(row_data)
    
    # Zamykanie przeglądarki
    browser.quit()
    
    # Tworzenie DataFrame z pobranych danych
    df = pd.DataFrame(table_data, columns=header)
    
    # Zapis DataFrame do pliku CSV
    df.to_excel(filename, index=False)
    
    print("Tabela została pobrana i zapisana w pliku 'population_by_country.xlsx'")
    

def get_country_code(country_name):
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    return None

def convert_population(pop):
    return int(pop.replace(',', ''))

def category_of_pop(pop):
    if pop > 1000000000:
        return "pop 1"
    elif pop > 10000000:
        return "pop 2"
    else:
        return "pop 3"
    
def df_to_dict(df):
    dict_of_countries = {}
    for row in df.iterrows():
        dict_of_countries[row[1][-2]] = row[1][2]
    return dict_of_countries
                

filename = r"D:\Users\TEK\Dokumenty\Posortowane\IT_Projekty\maping_global_population\population_by_country.xlsx"
try:
    table = pd.read_excel(filename)
except Exception as err:
    print(err)
    table = scrap_country_table(filename)
   
table['Country (or dependency)'] = table['Country (or dependency)'].apply(lambda x : corecting_country_names(x))
table['code'] = table['Country (or dependency)'].apply(lambda x : get_country_code(x))
table['Population\n(2020)'] = table['Population\n(2020)'].apply(lambda x : convert_population(x))
table["pop category"] = table['Population\n(2020)'].apply(lambda x : category_of_pop(x))

table_none = table[~table['code'].notnull()]
list(COUNTRIES.values())
table_not_none = table[table['code'].notnull()]

table_pop1 = table_not_none[table_not_none['pop category'] ==  'pop 1']
table_pop2 = table_not_none[table_not_none['pop category'] ==  'pop 2']
table_pop3 = table_not_none[table_not_none['pop category'] ==  'pop 3']

dict_pop1 = df_to_dict(table_pop1)
dict_pop2 = df_to_dict(table_pop2)
dict_pop3 = df_to_dict(table_pop3)
        
print(len(table_pop1), len(table_pop2), len(table_pop3))

wm_style = RotateStyle('#336699')
wm = World(style = wm_style)
wm.force_url_protocol = 'http'
wm.titlee = "Populacja na swiecie w 2020 roku (dane dla poszczególnych państw)"
wm.add('0 - 10 mln', dict_pop3)
wm.add('10 mln - 1 mld', dict_pop2)
wm.add('> 1 mld', dict_pop1)

wm.render_to_file(r"D:\Users\TEK\Dokumenty\Posortowane\IT_Projekty\maping_global_population\world.svg")
