import requests
import ssl
import logging
import xml.etree.ElementTree as ET

from currency_converter import CurrencyConverter


def currency_converter(value, source, target):
    logging.debug('Currency converter started')
    source = source.upper()
    target = target.upper()
    result = 0.0
    if hasattr(ssl, '_create_unverified_context'):
        logging.debug('SSL unverified context')
        ssl._create_default_https_context = ssl._create_unverified_context

    logging.debug('Value: {} - ' \
            'Source currency: {} - ' \
            'Target currency: {}'.format(value, source, target))

    if (source not in 'VND' and target not in 'VND'):  
        c = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
        result = c.convert(value, source, target)
    else:
        url = 'https://www.vietcombank.com.vn/ExchangeRates/ExrateXML.aspx'
        r = requests.get(url)

        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for element in root:
                symbol = str(element.attrib.get('CurrencyCode'))
                if symbol in source:
                    quote = float(element.attrib.get('Transfer'))
                    result = value * quote
                if symbol in target:
                    quote = float(element.attrib.get('Transfer'))
                    result = value / quote
        else:
            logging.warning('Request time out.')

    return result

