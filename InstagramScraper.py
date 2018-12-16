from random import choice
import json, csv, sys
import os.path

import requests
from bs4 import BeautifulSoup

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]


class InstagramScraper:

    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy,
                                                                                                 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']

        except Exception as e:
            raise e
        else:
            header_row = []
            row = []
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                    elif value:
                        results[key] = value




                    try:
                        value=value.encode('utf-8')
                    except:
                        value=value


                    header_row.append(key)
                    row.append(value)


        if (os.path.isfile('Data1.csv')) == False:
            with open('Data1.csv', 'a+') as outcsv:
                writer = csv.DictWriter(outcsv, fieldnames=header_row)
                writer.writeheader()

        cs_data = open('Data1.csv', 'a+')
        csvwriter = csv.writer(cs_data)
        csvwriter.writerow(row)
        cs_data.close()

    def profile_page_recent_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)

            json_da = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                'edges']
            # print(json_da)



            if (os.path.isfile('Data.csv'))==False:
                with open('Data.csv', 'a+') as outcsv:
                    writer = csv.DictWriter(outcsv, fieldnames=['id', 'caption', 'comment_count', 'timestamp',
                                                                'dimension_height', 'dimension_width', 'display_url',
                                                                'like_count'])
                    writer.writeheader()
            # file exists




            cs_data = open('Data.csv', 'a+')

            csvwriter = csv.writer(cs_data)

            count = 0
            for i in json_da:
                csvwriter.writerow([i['node']['id'], i['node']['edge_media_to_caption']['edges'][0]['node']['text'].encode('utf-8'),
                                    i['node']['edge_media_to_comment']['count'], i['node']['taken_at_timestamp'],
                                    i['node']['dimensions']['height'], i['node']['dimensions']['width'],
                                    i['node']['display_url'], i['node']['edge_liked_by']['count']])

            cs_data.close()

        except Exception as e:
            raise e

