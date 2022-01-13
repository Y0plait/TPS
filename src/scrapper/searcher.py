import asyncio
import json
import logging
import time
import aiohttp
from bs4 import BeautifulSoup


class TorrentSearcher():

    def __init__(self, name: str, language: str, quality: str):
        # Defining global variables
        '''
        name : the name of the movie,
        language : the language of the movie in a two letter format ('EN', 'FR' ...),
        quality : quality of the movie (1080, HD ...),
        use_proxy : boolean True or False
        '''

        logging.basicConfig(filename='./app.log', filemode='w',
                            format='%(asctime)s ; %(levelname)s: %(message)s', level=logging.INFO)

        self.name = name.replace(' ', '%20')
        self.language = language
        self.quality = quality

        logging.info(
            f'Name: {self.name}, Language: {self.language}, Quality: {self.quality}')

        # Load websites urls from sites.json
        with open('./sites.json', 'r') as json_file:
            websites_file = json.loads(json_file.read())

        # Extract urls from the json
        result_urls = list()
        for lang in websites_file['site']:
            for torrent_website_name in websites_file['site'][lang]:
                result_urls.append(
                    websites_file['site'][lang][torrent_website_name])

        # Store formatted urls in a var
        self.finals_url = [w.replace('data', self.name) if ('tpb' or 'pirate' or 'bay') in w else w.replace(
            'data', (self.name+"%20"+self.language)) for w in result_urls]

    def _get_search_pages(self) -> dict:
        '''
        Fetch all movies urls generated in the __init__ function
        Return a dict with the data of each sites
        '''
        # Using async to fetch the urls
        data = dict()

        async def get_search_results():

            async with aiohttp.ClientSession() as session:
                # Fetch search pages with asyncio
                for i in range(0, len(self.finals_url)):
                    surl = self.finals_url[i]
                    async with session.get(surl, headers={'User-Agent': 'Mozilla/5.0', 'Referer': self.finals_url[i][:self.finals_url[i].find('/', 8)]}) as resp:
                        data.update({surl: (await resp.text())})
                        logging.info(f'Fetched "{surl}"')

        # https://stackoverflow.com/a/62633450
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        asyncio.get_event_loop().run_until_complete(get_search_results())

        # return each website source code
        return data

    def _isolate_links(self, specific=False) -> dict:
        '''
        Isolate name, magnet link(s), size, number of seeders for each file available
        Return a dict with this format:

        {'name_parsed_in_the_website':
            {
                'location_of_the_desc_page': 'https...',
                'size_of_the_file': 'XX.X Xxb',
                'number_of_seeders': xxx
            },
            etc, etc
        }
        '''

        # Making a dict to store everything
        data = self._get_search_pages()
        movies = dict()

        for site_index in list(data):
            soup = BeautifulSoup(data[site_index], 'lxml')
            logging.info(f'Parsing {site_index}')
            # Tried many times to parse data from torrent9 websites but magnet links are javascript scripts ... and i was banned soo cannot work on that
            '''if ("torrent9") in site_index:
                tbody = soup.find('tbody')
                try:
                    
                    for trs in tbody.find_all('tr'):
                        name = trs.find(
                            'a', {'style': 'color:#000; font-size:12px; font-weight:bold;'}).text
                        a_dev = trs.find(
                            'a', {'style': 'color:#000; font-size:12px; font-weight:bold;'}, href=True)
                        href = a_dev['href']

                        size = trs.find(
                            'td', {'style': 'font-size:13px;text-align:right; padding-right:5px'}).text
                        seeders = trs.find('span', {'class': 'seed_ok'}).text

                        # if self.name.replace('%20', ' ').capitalize() in name.capitalize():
                        movies.update(
                            {name: {'location': [self.finals_url[i][:self.finals_url[i].find('/', 8)] for i in range(0, len(self.finals_url)) if ("torrent9") in self.finals_url[i]][0] + href,
                                    'size': size.replace('\u00a0', ''),
                                    'seeders': seeders,
                                    'magnet': ''}})

                except Exception as e:
                    # When there is not any <tr> to parse Bs return an AttributeError: TypeError
                    # So just ignore it
                    logging.warning(f'Exception: {e}')
                    pass'''

            if ("tpb" or "pirate" or "bay") in site_index:
                table = soup.find('table')
                try:
                    for trs in table.find_all('tr'):
                        # Dirty way to bypass the tr header
                        if ('<tr class="header">') not in str(trs):
                            name = trs.find('a', {'class': 'detLink'}).text
                            magnet = trs.find(
                                'a', {'title': "Download this torrent using magnet"}, href=True)
                            magnet = magnet['href']
                            metadata = trs.find(
                                'font', {'class': 'detDesc'}).text
                            size = metadata.split(',')[1].replace('Size ', '')
                            seeders = trs.find('td', {'align': 'right'}).text
                            a_dev = trs.find('div', {'class': 'detName'})
                            href = [a['href']
                                    for a in a_dev.select('a[href]')][0]
                            logging.info(magnet)
                            # if self.name.replace('%20', ' ').capitalize() in name.capitalize():
                            movies.update(
                                {name: {'location': href,
                                        'size': size.replace('\u00a0', ''),
                                        'seeders': seeders, 'magnet': magnet
                                        }}),
                            #

                        else:
                            pass

                except AttributeError or TypeError as e:
                    pass

            # Underwork
            if ("torlock") in site_index:
                table = soup.find('table', {
                    'class': 'table table-striped table-bordered table-hover table-condensed'})
                try:
                    for trs in table.find_all('tr'):
                        if str(trs.find('tr').parent) is not 'thead':
                            href = [a['href']
                                    for a in trs.select('a[href]')][0]
                            name = trs.find('b').text
                            size = trs.find('td', {'class': 'ts'})
                            seeders = trs.find('td', {'class': 'tf'})
                            movies.update({name: {'location': [self.finals_url[i][:self.finals_url[i].find('/', 8)] for i in range(0, len(self.finals_url)) if ("torlock") in self.finals_url[i]][0] + href,
                                                  'size': size,
                                                  'seeders': seeders}})
                        else:
                            pass
                except AttributeError as e:
                    logging.info(f'No more tr !! {e}')

        # If the name have to correspond perfectly (uppercased but you've understand)
        if specific:
            for mov in movies.keys():
                if not self.name.replace('%20', ' ').capitalize() in movies[mov].capitalize():
                    movies.pop(mov)
                else:
                    pass

        if not specific:
            pass

        logging.info(f'Found {len(list(movies))} torrents.')
        return movies

    def _get_magnet_links(self, **kwargs) -> dict:
        start = time.time()
        webpages = dict()
        movies = self._isolate_links()

        async def get_pages():
            async with aiohttp.ClientSession() as session:
                for name in list(movies):
                    async with session.get(movies[name]['location'], **kwargs) as resp:
                        webpages.update({name: {(await resp.text())}})
                        logging.info(f'fetched "{movies[name]["location"]}"')

        # https://stackoverflow.com/a/62633450
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        asyncio.get_event_loop().run_until_complete(get_pages())

        end = time.time()
        # for pages in list(webpages):
        #    soup = BeautifulSoup(webpages[pages])
        logging.info(f'Fetched {len(webpages)} in {end - start}')
        return movies
