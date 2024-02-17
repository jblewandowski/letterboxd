import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import json
import re

include_unrated = False

def get_films(user):
    films = []
    r = session.get(f'https://letterboxd.com/{user}/films/size/large/')
    r2 = BeautifulSoup(r.content, 'html.parser')
    pages = int(r2.find('div', class_='paginate-pages').ul.select('li')[-1].a.text)
    for page in range(pages):
        p = session.get(f'https://letterboxd.com/{user}/films/size/large/page/{page+1}')
        films.extend(BeautifulSoup(p.content, 'html.parser').find_all('li', class_='poster-container'))
    return films

def download_data(film_id):
    url1 = f'https://letterboxd.com/film/{film_id}/details/'
    url2 = f'https://letterboxd.com/csi/film/{film_id}/rating-histogram/'
    url3 = f'https://letterboxd.com/csi/film/{film_id}/stats/'
    return {f'html{i+1}' : BeautifulSoup(session.get(url).content, 'html.parser') for i, url in enumerate([url1, url2, url3])}

def extract_data(film_data):
    html1 = film_data['html1']
    html2 = film_data['html2']
    html3 = film_data['html3']

    jinfo = json.loads(html1.find('script', type="application/ld+json").text.split('\n')[2])
    try:
            film_data['releaseYear'] = int(jinfo['releasedEvent'][0]['startDate'])
            film_data['runTime'] = int(re.findall(r'[\d]+', html1.find('script', text=re.compile('runTime:')).text.split('runTime:')[1])[0])
    except:
        return False
    
    film_data['genre'] = jinfo['genre'] if 'genre' in jinfo else []
    film_data['countryOfOrigin'] = [i['name'] for i in jinfo['countryOfOrigin']] if 'countryOfOrigin' in jinfo else []

    for item in ['actors', 'director', 'productionCompany']:
        film_data[item] = [k['name'] for k in jinfo[item]] if item in jinfo else []
        film_data[f'{item}_id'] = [k['sameAs'] for k in jinfo[item]] if item in jinfo else []

    for item in ['writer', 'editor', 'producer', 'cinematography', 'composer']:
        try:
            members = html1.find('div', id='tab-crew').select(f'a[href*={item}]')
        except:
            members = []
        film_data[item] = [k.text for k in members]
        film_data[f'{item}_id'] = [k['href'] for k in members]

    film_data['reviewCount'] = jinfo['aggregateRating']['reviewCount'] if 'aggregateRating' in jinfo and 'reviewCount' in jinfo['aggregateRating'] else 0
    film_data['ratingValue'] = jinfo['aggregateRating']['ratingValue'] if 'aggregateRating' in jinfo and 'ratingValue' in jinfo['aggregateRating'] else None
    film_data['ratingCount'] = jinfo['aggregateRating']['ratingCount'] if 'aggregateRating' in jinfo and 'ratingCount' in jinfo['aggregateRating'] else 0

    film_data['originalLanguage'] = html1.find(href=re.compile('/films/language/')).text
    film_data['language'] = []
    for language in html1.find_all(href=re.compile('/films/language/')):
        if language.text not in film_data['language']:
            film_data['language'].append(language.text)

    # Could not be bothered to fix the try except hellscape below, and I mean if it works it works right?
    try:
        film_data['theme'] = [i.text for i in html1.find_all('a', {'class':'text-slug', 'href':(re.compile('films/theme/'))}) + html1.find_all('a', {'class':'text-slug', 'href':(re.compile('films/mini-theme/'))})]
    except:
        film_data['theme'] = []

    try:
        film_data['fans'] = int(html2.find('a', class_='all-link more-link').text.split(' ')[0])
    except:
        try:
            film_data['fans'] = int(float(html2.find('a', class_='all-link more-link').text.split(' ')[0][:-1])*1000)
        except:
            film_data['fans'] = 0

    for item, loc, err in zip(['watches', 'likes', 'lists'], [8, 8, 6], [1, 0, 0]):
        try:
            film_data[item] = int(html3.find('li', {'class':f'stat filmstat-{item}'}).a['title'][:-loc].split(' ')[-1].replace(',', ''))
        except:
            film_data[item] = err

    for item in ['html1', 'html2', 'html3']:
        del film_data[item]
    
    return film_data

def main(film):
    film_id = film.div['data-film-slug']
    film_data = {}
    film_data['film_id'] = film_id
    try:
        try: 
            film_data['userRating'] = int(film.p.span['class'][-1].split('-')[1])
        except:
            if include_unrated:
                film_data['userRating'] = None
            else:
                return film_id, False
        film_data['title'] = film.div.img['alt']
        film_data['dateRated'] = str(film.p.time['datetime'])[0:10]
        film_data = {**film_data, **download_data(film_id)}
    except:
        return film_id, False
    
    # print(film_data['title'])
    film_data = extract_data(film_data)
    return film_id, film_data

def scrape(user):
    global session
    session = requests.session()
    t = time.perf_counter()
    films = get_films(user)
    with ThreadPoolExecutor(max_workers=64) as p:
        results = p.map(main, films)
    film_dict = {film_id : result for film_id, result in results if result}
    t = time.perf_counter() - t
    return film_dict, t

# I tried experimenting with asynchronous http requests to get this to be even faster, but didn't have any success.
# Oh well, it's already pretty fast as it is, and I don't want to risk Letterboxd banning my IP.
# All in all, I'm pretty happy with this code.