import time
import os
import sys
import ssl

from currency_converter import CurrencyConverter

def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    print(sys.path[0])
    print(dname)
    print('Current path: {}'.format(os.getcwd()))
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    c = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
    args = "100 usd eur"
    elements = args.split()
    value = int(elements[0])
    scurrency = elements[1].upper()
    tcurrency = elements[2].upper()
    text = c.convert (value, scurrency, tcurrency)

    print('{0:.2f}'.format(text))

    time.sleep(100000)

if __name__ == '__main__':
    main()