#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/10

import time
import requests
from libs import log

def http_client(*args, **kwargs):
    """
    :param args: 
    :param kwargs: 
    :return: str not unicode
    """
    symbol = kwargs['symbol']
    url = kwargs['url']
    headers = kwargs['headers'] if "headers" in kwargs else {}
    #cookies = kwargs['cookies']
    times =3 #try three times
    while times > 0:
        try:
            r= requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.ConnectionError:
            log.logger.error('HTTP %s no-connection' % symbol)
        except requests.exceptions.HTTPError:
            log.logger.error('HTTP %s status %d' % (symbol, r.status_code))
        except requests.exceptions.Timeout:
            log.logger.error('HTTP %s time out' % symbol)
        except requests.exceptions.TooManyRedirects:
            log.logger.error('HTTP %s too many redirects' % symbol)
        except Exception:
            times -= 1
            time.sleep(3)
            continue
        else:
            log.logger.info('HTTP %s OK' % symbol)
            break
    if times <= 0:
        return None
    else:
        return r.content

