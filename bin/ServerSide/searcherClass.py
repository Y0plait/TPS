import asyncio
import json
import logging

import aiohttp
from bs4 import BeautifulSoup


class TorrentSearcher():

    def __init__(self, name: str, language: str, quality: str):
        # Defining global variables
        '''
        name : the name of the movie,
        language : the language of the movie in a two letter format ('EN', 'FR' ...),
        quality : quality of the movie (1080, HD ...),
        '''

        logging.basicConfig(filename='./app.log', filemode='w',
                            format='%(asctime)s ; %(levelname)s: %(message)s', level=logging.DEBUG)

        self.name = name.replace(' ', '%20')
        self.language = language
        self.quality = quality

        logging.info(
            f'Name: {self.name}, Language: {self.language}, Quality: {self.quality}')

        # Load websites urls from sites.json
        with open('./sites.json', 'r') as json_file:
            websites_file = json.loads(json_file.read())

        # Extract urls from the json in function of the language
        result_urls = list()
        for lang in websites_file['site']:
            for torrent_website_name in websites_file['site'][lang]:
                result_urls.append(
                    websites_file['site'][lang][torrent_website_name])

        # Store formatted urls in a var
        self.finals_url = [
            w.replace('data', (self.name)) for w in result_urls]
        # +'%20'+self.language

    def parse_movie_links(self, output_file=None):
        # Using async to fetch the urls
        data = dict()

        async def get_search_results():

            async with aiohttp.ClientSession() as session:

                for i in range(0, len(self.finals_url)):
                    surl = self.finals_url[i]
                    async with session.get(surl) as resp:
                        data.update({surl: (await resp.text())})
                        logging.info(f'Fetched "{surl}"')

        asyncio.get_event_loop().run_until_complete(get_search_results())

        # Making a dict to store everything
        movies = dict()

        for site_index in list(data):
            soup = BeautifulSoup(data[site_index], 'lxml')
            logging.info(f'Parsing {site_index}')
            # Parsing data for torrent9's websites:
            if ("torrent9") in site_index:
                data1 = soup.find('tbody')
                try:
                    for trs in data1.find_all('tr'):

                        name = str(
                            trs.find('a', {'style': "color:#000; font-size:12px; font-weight:bold;"}).text)
                        href = [a['href'] for a in trs.select('a[href]')][0]
                        size = trs.find_all(style="font-size:12px")[1].text
                        seeders = trs.find('span', {'class': "seed_ok"}).text

                        # if the name found in the <td> is the same as the one given as an argument then:
                        if self.name.replace('%20', ' ').capitalize() in name.capitalize():
                            movies.update(
                                {name: {'location': [self.finals_url[i][:self.finals_url[i].find('/', 8)] for i in range(0, len(self.finals_url)) if ("torrent9") in self.final_urls[i]] + href,
                                        'size': size,
                                        'seeders': seeders}})

                except AttributeError as e:
                    # When there is not any <tr> to parse Bs return an AttributeError: TypeError
                    # So just ignore it
                    logging.warning(f'No more <tr> to parse !! {e}')
                    pass

            if ("tpb") in site_index:
                table = soup.find('table')
                try:
                    for trs in table.find_all('tr'):
                        # Dirty way to bypass the tr header
                        if ('<tr class="header">') not in str(trs):
                            name = trs.find('a', {'class': 'detLink'}).text
                            magnet = trs.find(
                                'a', {'title': "Download this torrent using magnet"})
                            metadata = trs.find(
                                'font', {'class': 'detDesc'}).text
                            size = metadata.split(',')[1].replace('Size ', '')
                            seeders = trs.find('td', {'align': 'right'}).text
                            a_dev = trs.find('div', {'class': 'detName'})
                            href = [a['href']
                                    for a in a_dev.select('a[href]')][0]

                            if self.name.replace('%20', ' ').capitalize() in name.capitalize():
                                movies.update(
                                    {name: {'location': href, 'size': size, 'seeders': seeders}}),  # , 'magnet': magnet

                        else:
                            pass

                except AttributeError as e:
                    pass

        logging.info(f'Found {len(list(movies))} torrents.')
        return movies
