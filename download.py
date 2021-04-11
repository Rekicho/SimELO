import requests
from bs4 import BeautifulSoup
import re
import json

por_dict = {
    'teams': [],
    'schedule': []
}

team_name_dict = {
    'Sporting CP': 'Sporting',
    'FC Porto': 'Porto',
    'SL Benfica': 'Benfica',
    'SC Braga': 'Braga',
    'FC P.Ferreira': 'PacosFerreira',
    'Vitória SC': 'Guimaraes',
    'Santa Clara': 'SantaClara',
    'Moreirense FC': 'Moreirense',
    'Portimonense': 'Portimonense',
    'Gil Vicente FC': 'GilVicente',
    'CD Tondela': 'Tondela',
    'Rio Ave FC': 'RioAve',
    'FC Famalicão': 'Famalicao',
    'Belenenses SAD': 'Belenenses',
    'Boavista FC': 'Boavista',
    'Marítimo M.': 'Maritimo',
    'SC Farense': 'Farense',
    'CD Nacional': 'Nacional'    
}

r = requests.get('http://clubelo.com/POR')
soup = BeautifulSoup(r.text, 'html.parser')

p = re.compile(r'Home Field Advantage: (.*) Elo points.')
m = p.search(r.text)
por_dict['HFA'] = float(m.group(1))

sidebarCountries = soup.find('table', {'class': 'liste'}).find_all('tr')

numberTeams = None

for i, country in enumerate(sidebarCountries):
    if numberTeams is not None:
        if numberTeams == 0:
            break

        p = re.compile(r'href="/(.*?)".*(\d{4})')
        m = p.search(str(country))

        por_dict['teams'].append({
            'name': m.group(1),
            'elo': int(m.group(2))
        })

        numberTeams -= 1

    tag_i = country.find('i')

    if tag_i:
        header = sidebarCountries[i - 1].find('a')

        if header and '/POR' in str(header):
            p = re.compile(r'(\d*) teams')
            m = p.search(tag_i.text)
            numberTeams = int(m.group(1))

r = requests.get('https://www.ligaportugal.pt/pt/liga/classificacao/20202021/liganos')
soup = BeautifulSoup(r.text, 'html.parser')
rows = soup.find('tbody').find_all('tr')[1:]

for row in rows:
    cells = row.find_all('td')

    team_name = team_name_dict[cells[2].text.strip()]
    points = int(cells[-1].text.strip())

    next((x for x in por_dict['teams'] if x['name'] == team_name), None)['points'] = points

r = requests.get('https://www.ligaportugal.pt/pt/liga/calendario/completo/20202021/liganos')
soup = BeautifulSoup(r.text, 'html.parser')
rows = soup.find_all('tr')

for row in rows:
    cells = row.find_all('td')

    if 'vs' in cells[1].text:
        team_home = cells[0].text.strip()
        team_away = cells[2].text.strip()

        por_dict['schedule'].append({
            'home': team_name_dict[team_home],
            'away': team_name_dict[team_away]
        })

with open('data/POR.json', 'w') as output:
    json.dump(por_dict, output)