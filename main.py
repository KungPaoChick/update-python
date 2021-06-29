import requests
import os
import shutil
import wget
import colorama
import platform
from colorama import Fore, Style
from bs4 import BeautifulSoup


class Python_Update:
    
    def __init__(self, py_link):
        self.py_link = py_link

    def get_update(self):
        try:
            with requests.get(self.py_link) as response:
                response.raise_for_status()
                page_soup = BeautifulSoup(response.text, 'html.parser')

            release = []
            for div in page_soup.findAll('div', {'class': 'download-os-windows'}):
                for version in div.findAll('a', {'class': 'button'}):
                    lt_release = version.text.split()[-1]

                    print(Fore.GREEN, f'[*] Latest Release: {lt_release}', Style.RESET_ALL)
                    release.extend((lt_release, version['href']))
            
            if not release[0] == platform.python_version():
                print(f'Current version: {platform.python_version()} - New Version: {release[0]}')
                Python_Update(self.py_link).download_release(release[1])
            else:
                print(Fore.YELLOW, '[!] Your Python version is up to date!', Style.RESET_ALL)

        except requests.HTTPError as err:
            print(Fore.RED, f'[!!] Something went wrong! {err}', Style.RESET_ALL)

    def download_release(self, link):
        try:
            py_filename = link.split('/')[-1]
            wget.download(link, py_filename)
            
            source = os.path.join(os.getcwd(), py_filename)
            target = os.path.join(os.path.expanduser('~'), 'Downloads')

            shutil.move(source, target)
            if py_filename in os.listdir(target):
                print(Fore.GREEN, f"\n[*] {py_filename} has been downloaded", Style.RESET_ALL)
                print(Fore.YELLOW, f'\n[!] {py_filename} is located in: {os.path.join(target, py_filename)}')
        except Exception as err:
            print(Fore.RED, f'[!!] Something went wrong! {err}', Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()
    Python_Update('https://www.python.org/downloads/').get_update()
