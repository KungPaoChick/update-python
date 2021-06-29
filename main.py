import requests
import os
import wget
import colorama
from colorama import Fore, Style
from bs4 import BeautifulSoup as soup


class Python_Update:
    
    def __init__(self, py_link):
        self.py_link = py_link

    def get_update(self):
        try:
            import platform
            with requests.get(self.py_link) as response:
                response.raise_for_status()
                page_soup = soup(response.text, 'html.parser')

            release = []
            for div in page_soup.findAll('div', {'class': 'download-os-windows'}):
                for version in div.findAll('a', {'class': 'button'}):
                    release.extend((version.text.split()[-1], version['href']))
                    print(Fore.GREEN, f'[*] Latest Release: {version.text.split()[-1]}', Style.RESET_ALL)
            
            if not release[0] == platform.python_version():
                print(f'Current version: {platform.python_version()} - New Version: {release[0]}')
                Python_Update(self.py_link).download_update(release[1])
            else:
                print(Fore.YELLOW, '[!] Your Python version is up to date!', Style.RESET_ALL)
        except requests.HTTPError as err:
            print(Fore.RED, f'[!!] Something went wrong! {err}', Style.RESET_ALL)

    def download_update(self, link):
        try:
            wget.download(link, link.split('/')[-1])
            
            if link.split('/')[-1] in os.listdir(os.path.join(os.getcwd())):
                print(Fore.GREEN, f"\n[*] {link.split('/')[-1]} has been downloaded", Style.RESET_ALL)
        except Exception as err:
            print(Fore.RED, f'[!!] Something went wrong! {err}', Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()
    Python_Update('https://www.python.org/downloads/').get_update()
