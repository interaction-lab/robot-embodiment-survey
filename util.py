import os
import urllib.request

from bs4 import BeautifulSoup
from flask import json

from schema import Robot


def parse_robots_db(db):
    URL = 'https://robots.ieee.org/robots/'
    ROBOT_IMG_DIR = 'robots'
    robots = {}
    with open('ieee_robots.html', 'r') as robots_file:
        soup = BeautifulSoup(robots_file)
        soup.prettify()
        for div in soup.findAll('div'):
            if div.get('id') == 'robotResults':
                children = div.findChildren('img', recursive=True)
                for img in children:
                    robots[img.get('alt')] = {
                        'short_name': img.get('data-src').split('/')[-1].split('-thumb')[0],
                        'remote_url': ''.join([URL, img.get('data-src').split('../robots/')[-1]]),
                    }
                    robots[img.get('alt')]['local_path'] = os.path.join(ROBOT_IMG_DIR,
                                                                        robots[img.get('alt')]['short_name'] + '.jpg')

        if not os.path.exists(ROBOT_IMG_DIR):
            os.mkdir(ROBOT_IMG_DIR)
            for robot, params in robots.items():
                print(params['remote_url'])
                urllib.request.urlretrieve(params['remote_url'], params['local_path'])

        for robot, params in robots.items():
            r = Robot()
            r.name = robot
            for k, v in params.items():
                r.__setattr__(k, v)
            print("adding robot " + repr(r))
            db.session.add(r)
        db.session.commit()
        db.session.flush()

        return json.dumps(robots)
