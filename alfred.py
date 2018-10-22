import os
import logging
import time
import configparser

from telegram.ext import Updater
from telegram.ext import CommandHandler

import bitmexmanager as bitmex
import msfeed

def main():
    #set path
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    #config logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler('{0}.log'.format(time.strftime("alfred-%Y-%m-%d"))),
                            logging.StreamHandler()
                            ]
                        )
    logging.info('Virtual Assistent started.')
    logging.info('Working directory: {}'.format(dname))

    cp = configparser.RawConfigParser()  
    logging.debug('Read config.txt')
    cp.read('config.txt')

    #create updater and pass token
    logging.debug('Pass API token to Updater')
    updater = Updater(token=cp.get('telegram', 'TOKEN'))

    #Dispatcher to register handlers
    dispatcher = updater.dispatcher

    #Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('btc', btc))
    dispatcher.add_handler(CommandHandler('last_price', btc_last_price))
    dispatcher.add_handler(CommandHandler('funding', btc_funding))
    dispatcher.add_handler(CommandHandler('cancel_all_orders', bitmex_cancel_orders))
    dispatcher.add_handler(CommandHandler('manga', manga))

    logging.info(dispatcher)

    updater.start_polling()
    updater.idle()

def start(bot, update):
    logging.info('Start requested.')
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def help(bot, update):
    command_list = ['/start', '/manga', '/btc', '/last_price',
                    '/funding', '/bitmex_cancel_orders'
                    ]
    logging.info('Help requested.')
    text = 'You can use the following commands:\n'

    for command in command_list:
        text += command + '\n'

    bot.send_message(chat_id=update.message.chat_id, text=text)

def btc(bot, update):
    logging.info('BTC information requested.')
    requ = bitmex.get_funding('XBTUSD')
    text = 'XBT/USD last price: {}\nNext funding rate: {}\nPredicted funding rate: {}'.format(
        bitmex.get_last_price('BTC/USD'),
        requ['fundingRate'],
        requ['indicativeFundingRate']
        )

    bot.send_message(chat_id=update.message.chat_id, text=text)    

def btc_last_price(bot, update):
    logging.info('Last Price requested.')
    last_price = 'XBT/USD last price: {}'.format(bitmex.get_last_price('BTC/USD'))
    bot.send_message(chat_id=update.message.chat_id, text=last_price)


def btc_funding(bot, update):
    logging.info('Funding requested.')
    requ = bitmex.get_funding('XBTUSD')

    text = '{}\nNext funding rate: {}\nPredicted funding rate: {}'.format(
        requ['symbol'], 
        requ['fundingRate'],
        requ['indicativeFundingRate']
        )
    bot.send_message(chat_id=update.message.chat_id, text=text)


def bitmex_cancel_orders(bot, update):
    logging.info('Cancel all orders requested.')
    bitmex.cancel_all_orders()
    bot.send_message(chat_id=update.message.chat_id, text='All open orders cancelled.')


def manga(bot, update):
    logging.info('Manga updates requested.')
    manga_update = msfeed.check_manga()
    bot.send_message(chat_id=update.message.chat_id, text=manga_update)


if __name__ == '__main__':
    main()