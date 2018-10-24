from curconverter import currency_converter as c

def main():
    test = c(100, 'usd', 'vnd')
    print('100 USD = {0:.2f} VND '.format(test))
    test = c(100000, 'vnd', 'eur')
    print('100000 VND = {0:.2f} EUR '.format(test))
    test = c(1, 'eur', 'vnd')
    print('1 EUR = {0:.2f} VND '.format(test))
    test = c(1, 'usd', 'vnd')
    print('1 USD = {0:.2f} VND '.format(test))
    test = c(10, 'eur', 'usd')
    print('10 EUR = {0:.2f} USD '.format(test))

if __name__ == '__main__':
    main()