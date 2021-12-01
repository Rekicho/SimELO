import requests
from bs4 import BeautifulSoup
import re
import json

por_dict = {
    'teams': [],
    'schedule': [],
    'h2h': {},
    'temp_h2h': {}
}

team_name_dict = {
    'FC Porto': 'Porto',
    'SL Benfica': 'Benfica',
    'Sporting CP': 'Sporting',
    'SC Braga': 'Braga',
    'Santa Clara': 'SantaClara',
    'Moreirense FC': 'Moreirense',
    'FC Famalicão': 'Famalicao',
    'Vitória SC': 'Guimaraes',
    'FC P.Ferreira': 'PacosFerreira',
    'Boavista FC': 'Boavista',
    'Gil Vicente FC': 'GilVicente',
    'Belenenses SAD': 'Belenenses',
    'Portimonense': 'Portimonense',
    'Marítimo M.': 'Maritimo',
    'CD Tondela': 'Tondela',
    'FC Vizela': 'Vizela',
    'Estoril Praia': 'Estoril',
    'FC Arouca': 'Arouca'    
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

r = requests.get('https://www.ligaportugal.pt/pt/liga/classificacao/20212022/ligaportugalbwin')
soup = BeautifulSoup(r.text, 'html.parser')
rows = soup.find('tbody').find_all('tr')[1:]

for row in rows:
    cells = row.find_all('td')

    team_name = team_name_dict[cells[2].text.strip()]

    try:
        points = int(cells[-1].text.strip())

    except:
        points = 0

    next((x for x in por_dict['teams'] if x['name'] == team_name), None)['points'] = points

r = requests.get('https://www.ligaportugal.pt/pt/liga/calendario/completo/20212022/ligaportugalbwin')
soup = BeautifulSoup(r.text, 'html.parser')
rows = soup.find_all('tr')

for row in rows:
    cells = row.find_all('td')
    team_home = team_name_dict[cells[0].text.strip()]
    team_away = team_name_dict[cells[2].text.strip()]

    ordered = team_home + team_away if team_home <= team_away else team_away + team_home

    if 'vs' in cells[1].text:
        por_dict['schedule'].append({
            'home': team_home,
            'away': team_away
        })

    else:
        p = re.compile(r'(\d*) - (\d*)')
        m = p.search(cells[1].text.strip())

        goals_home = int(m.group(1))
        goals_away = int(m.group(2))
        home_points = 3 if goals_home > goals_away else 1 if goals_home == goals_away else 0
        away_points = 0 if goals_home > goals_away else 1 if goals_home == goals_away else 3

        if ordered in por_dict['temp_h2h']:
            info = por_dict['temp_h2h'][ordered]

            info[team_home + '_points'] += home_points
            info[team_home + '_home_goals'] += goals_home
            info[team_away + '_points'] += away_points
            info[team_away + '_away_goals'] += goals_away

            if info[team_home + '_points'] > info[team_away + '_points']:
                winner = team_home
            
            elif info[team_home + '_points'] < info[team_away + '_points']:
                winner = team_away

            elif info[team_home + '_home_goals'] + info[team_home + '_away_goals'] > \
                info[team_away + '_home_goals'] + info[team_away + '_away_goals']:
                winner = team_home

            elif info[team_home + '_home_goals'] + info[team_home + '_away_goals'] < \
                info[team_away + '_home_goals'] + info[team_away + '_away_goals']:
                winner = team_away

            elif info[team_home + '_away_goals'] > info[team_away + '_away_goals']:
                winner = team_home

            elif info[team_home + '_away_goals'] < info[team_away + '_away_goals']:
                winner = team_away

            else:
                continue

            del por_dict['temp_h2h'][ordered]
            por_dict['h2h'][ordered] = winner

        else:
            por_dict['temp_h2h'][ordered] = {
                team_home + '_points': home_points,
                team_home + '_home_goals': goals_home,
                team_home + '_away_goals': 0,
                team_away + '_points': away_points,
                team_away + '_home_goals': 0,
                team_away + '_away_goals': goals_away
            }

with open('data/POR.json', 'w') as output:
    json.dump(por_dict, output)