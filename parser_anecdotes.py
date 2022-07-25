#!/usr/bin/env python
# -*- coding: utf-8 -*-

# parsing libraries
import requests
from bs4 import BeautifulSoup

# library in order not to overload the server
from time import sleep


def stirletz_parser():
    """
    function for parsing all anecdotes from anekdot.ru on the topic Stirlets
    """

    data = []
    delimiter = '\n'

    for p in range(1 , 5):  # running through all the pages
        url = f'https://www.anekdot.ru/tags/%D0%A8%D1%82%D0%B8%D1%80%D0%BB%D0%B8%D1%86/{p}'  # parser
        r = requests.get(url)
        sleep(3)
        soup = BeautifulSoup(r.text , 'lxml')
        anekdots = soup.findAll('div' , class_ = 'text')

        for line_break in soup.findAll('br'):  # solve the soup.text problem, which eats up the html tag <br>
            line_break.replaceWith(delimiter)

        for anekdot in anekdots:  # add all the anecdotes from the page
            strings = soup.get_text().split(delimiter)
            data.append(anekdot.text)

    return data

def sport_parser():
    """
    function for parsing all anecdotes from anekdot.ru on the topic sport
    """

    data = []
    delimiter = '\n'

    for p in range(1 , 22):  # running through all the pages
        url = f'https://www.anekdot.ru/tags/%D1%81%D0%BF%D0%BE%D1%80%D1%82/{p}'  # parser
        r = requests.get(url)
        sleep(3)
        soup = BeautifulSoup(r.text , 'lxml')
        anekdots = soup.findAll('div' , class_ = 'text')

        for line_break in soup.findAll('br'):  # solve the soup.text problem, which eats up the html tag <br>
            line_break.replaceWith(delimiter)

        for anekdot in anekdots:  # add all the anecdotes from the page
            strings = soup.get_text().split(delimiter)
            data.append(anekdot.text)

    return data

def student_parser():
    """
    function for parsing all anecdotes from anekdot.ru on the topic student
    """

    data = []
    delimiter = '\n'

    for p in range(1 , 20):  # running through all the pages
        url = f'https://humornet.ru/anekdot/pro-studentov/page/{p}/'  # parser
        r = requests.get(url)
        sleep(3)
        soup = BeautifulSoup(r.text , 'lxml')
        anekdots = soup.findAll('div' , class_ = 'text')

        for line_break in soup.findAll('br'):  # solve the soup.text problem, which eats up the html tag <br>
            line_break.replaceWith(delimiter)

        for anekdot in anekdots:  # add all the anecdotes from the page
            strings = soup.get_text().split(delimiter)
            data.append(anekdot.text)

    return data

if __name__ == '__main__':

    anekdot = stirletz_parser()
    print(anekdot)
    anekdot = sport_parser()
    print(anekdot)
    anekdot = student_parser()
    print(anekdot)
