# Web Scraping using BeautifulSoup

The contents in this folder show examples of how to use [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (BS) to scrape web content.
Note that BeautifulSoup works best with websites that only use HTML code, while websites running Javascript, PHP or similar code might not play nicely with BS, and you might be unable to scrape the information you are aiming for.


## XKCD
The file [xkcd.py](./xkcd.py) shows a simple application of how to use BeautifulSoup to scrape information from the [XKCD website](https://xkcd.com/).

The class `XkcdComic` provides a Python interface to comic-related information: the object is instantiated with the ID number of the comic (found in the URL) and saves the title, the caption and the link to the image file.
The class has a method that offers to download the image file to local disk.

The code also shows an example of how to use the `XkcdComic` class to download comics and create a simple textual log of the files the user downloads.
There is also an example of how to be gentle on web servers, waiting some time between requests to prevent excessive server load (and its consequences, e.g., IP address ban).

You can freely use the [xkcd.py](./xkcd.py) file as long as you note [Randall Munroe's License notice](https://xkcd.com/license.html), as he is the creator and the owner of the comics.


# Disclaimer
I want the reader to be aware of the following: **web scraping might put you into trouble**.
It might be illegal activity in your Country, it might violate a website Terms and Conditions or it might simply be considered unethical.
Whatever you do with the material you find here, make sure you understand the risks and the responsibility that you are taking on.
I suggest you read [this zine](https://www.crummy.com/software/BeautifulSoup/zine/), written by the developer of Beautiful Soup.
Let me also remind you that the code you find here is covered by the [MIT license](../LICENSE), meaning in particular that I do not share the responsibility of what _you_ do with my code.
