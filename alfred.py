import os
import logging
import time
import configparser
import ssl

from telegram.ext import Updater
from telegram.ext import CommandHandler

from curconverter import currency_converter as c

def main():
    #set path
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    #config logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler('{0}.log'.format(
                                time.strftime("alfred-%Y-%m-%d"))),
                            logging.StreamHandler()
                            ]
                        )
    logging.info('Virtual Assistent started.')
    logging.info('Working directory: {}'.format(dname))


    #create updater and pass token
    logging.debug('Pass API token to Updater')
    updater = Updater(token=cp.get('telegram', 'TOKEN'))

    #Dispatcher to register handlers
    dispatcher = updater.dispatcher

    #Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('btc', btc))
    dispatcher.add_handler(
        CommandHandler('currency', currency_converter, pass_args=True))

    logging.info(dispatcher)

    updater.start_polling()
    updater.idle()

def start(bot, update):
    logging.info('Start requested.')
    bot.send_message(chat_id=update.message.chat_id, 
        text="I'm a bot, please talk to me!")


def help(bot, update):
    command_list = ['/btc', '/currency value base target'
                    ]
    logging.info('Help requested.')
    text = 'You can use the following commands:\n'

    for command in command_list:
        text += command + '\n'

    bot.send_message(chat_id=update.message.chat_id, text=text)

def btc(bot, update):
    logging.info('BTC information requested.')
    requ = ""
    text = 'XBT/USD last price: {0}\nNext funding rate: {1:.4f}%' \
            '\nPredicted funding rate: {2:.4f}%'.format(
                bitmex.get_last_price('BTC/USD'),
                requ['fundingRate'] * 100,
                requ['indicativeFundingRate'] * 100)
    bot.send_message(chat_id=update.message.chat_id, text=text)    



def currency_converter(bot, update, args):
    logging.info('Currency conversion requested.')
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    logging.debug(args)
    value = float(args[0])
    base = args[1].upper()
    target = args[2].upper()
    
    result = c(value, base, target)
    text = '{0:.2f} {1} = {2:.2f} {3}'.format(value, base, result, target)
    bot.send_message(chat_id=update.message.chat_id, text=text)


if __name__ == '__main__':
    main()