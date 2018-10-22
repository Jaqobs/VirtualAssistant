import logging
import time
import msfeed
import bitmexmanager as bitmex
from telegram.ext import Updater
from telegram.ext import CommandHandler

def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler('{0}.log'.format(time.strftime("alfred-%Y-%m-%d"))),
                            logging.StreamHandler()
            ])
    logging.info('Virtual Assitent started.')
    #create updater and pass token
    updater = Updater(token='674576910:AAG1zR1LV0yMdm9v2DWei4Jla_PgLwskkzY')

    #Dispatcher to register handlers
    dispatcher = updater.dispatcher

    #Handlers
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('last_price', btc_last_price))
    dispatcher.add_handler(CommandHandler('cancel_all_orders', bitmex_cancel_orders))
    dispatcher.add_handler(CommandHandler('manga', manga))

    updater.start_polling()
    updater.idle()

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def btc_last_price(bot, update):
    last_price = 'XBT/USD last price is {}'.format(bitmex.get_last_price('BTC/USD'))
    bot.send_message(chat_id=update.message.chat_id, text=last_price)

def bitmex_cancel_orders(bot, update):
    bitmex.cancel_all_orders()
    bot.send_message(chat_id=update.message.chat_id, text='All open orders cancelled.')

def manga(bot, update):
    manga_update = msfeed.check_manga()
    bot.send_message(chat_id=update.message.chat_id, text=manga_update)

if __name__ == '__main__':
    main()