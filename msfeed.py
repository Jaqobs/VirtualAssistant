import feedparser
import requests
import ssl
import logging

def check_manga():
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    url = 'https://readms.net/rss'
    feed = feedparser.parse(url)
    mangalist = ['One Piece', 'My Hero Academia', 'One-Punch Man', 'Attack on Titan', 'The Promised Neverland']
    answer = ''

    #check items in feed
    for item in feed.entries:
        for manga in mangalist:
            if manga in str(item.title):
                answer += str(item.title) + ' ' + str(item.updated) + '\n' + str(item.link) + '\n---------------------\n'
                logging.info('{} - last updated: {}'.format(str(item.title), str(item.updated)))

    return answer