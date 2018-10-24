import feedparser
import ssl
import logging

def check_manga():
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    url = 'https://readms.net/rss'
    feed = feedparser.parse(url)
    mangalist = [
                 'One Piece', 'My Hero Academia', 'One-Punch Man', 
                 'Attack on Titan', 'Boruto', 'Shokugeki no Souma',
                 'The Promised Neverland'
                ]

    res = []
    #check items in feed
    for item in feed.entries:
        for manga in mangalist:
            if manga in str(item.title):
                res.append({'title' : str(item.title), 
                            'timestamp' : str(item.updated), 
                            'url' : str(item.link)
                           })
                logging.info('{} - last updated: {}'.format(str(item.title), 
                                                            str(item.updated))
                            )

    return res