import feedparser
import ssl
import logging

def check_manga():
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    url = 'https://mangadex.org/rss/follows/Qt5uvARmBdUk78wxfGX3cZCH2S9Dshz4'
    feed = feedparser.parse(url)

    res = []
    #check items in feed
    temp_list = []
    #check feed
    for item in feed.entries:
      if (str(item.title).split("-")[0] not in temp_list):
        res.append({'title' : str(item.title), 
                     'timestamp' : str(item.updated), 'url' : str(item.link)
                            })
        temp_list.append(str(item.title).split("-")[0])
        logging.debug('{} - last updated: {}'.format(str(item.title), 
                                                            str(item.updated)))
      else:
        logging.debug('{} already in list'.format(str(item.title)))
        continue
                
    return res