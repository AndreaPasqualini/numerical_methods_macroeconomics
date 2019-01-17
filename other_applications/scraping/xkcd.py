"""
This code showcases the use of BeautifulSoup for pedagogical purposes. It
shows the way HTML code is parsed. It gives an idea about the way you can
navigate an HTML tree.
Read this before using BeautifulSoup:
https://www.crummy.com/software/BeautifulSoup/zine/
"""

from requests import get
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from time import sleep


class XkcdComic:
    """
    This class connects to https://xkcd.com/ and fetches data related to
    comics on that website. The HTML of the page is obtained using
    requests.get(). Parsing of the HTML code is done using BeautifulSoup.
    Retrieval of images is done using urllib.request.urlretrieve().
    The class offers a method to save images on disk. Please note that terms
    at https://xkcd.com/license.html apply at all times. The images are not
    my work. Only this code is mine.
    """

    def __init__(self, comic_number):
        self.number = str(comic_number)
        self.url = 'https://xkcd.com/' + self.number + '/'
        self._webpage = get(self.url)
        self._soup = BeautifulSoup(self._webpage.text, 'html.parser')
        self._container = self._soup.find('div', {'id': 'comic'})
        self._img_url = 'https:' + self._container.img['src']
        self._png_name = self._img_url.split('/')[-1]
        self.caption = self._container.img['title']
        self.title = self._soup.find('div', {'id': 'ctitle'}).text

    def save_img_to_disk(self, directory='./', filename=None):
        if filename is None:
            filename = self._img_url.split('/')[-1]
        if directory[-1] is not '/':
            directory += '/'
        urlretrieve(self._img_url, directory + filename)


if __name__ == '__main__':

    dir = 'C:/Users/Andrea/Pictures/xkcd/'
    numbers = [i for i in range(1900, 1968)]

    with open((dir + 'index.txt'), mode='w', encoding='utf-8') as index:
        index.write('Index of comics (w/captions) \n\n\n')

    for no in numbers:

        comic = XkcdComic(no)

        print('Saving to disk comic no. {}: {}'.format(no, comic.title))
        fname = '{}-{}'.format(no, comic._png_name)
        comic.save_img_to_disk(directory=dir,
                               filename=fname)
        sleep(1)  # pause execution for 1 second

        with open((dir + 'index.txt'), mode='a', encoding='utf-8') as index:
            index.write('#{}, {}: {}\n\n'.format(comic.number,
                                                 comic.title,
                                                 comic.caption))
