import os
import json
import urllib
import urllib2

class Venmo:


    def __init__(self):
        self.__paymentUrl__ = "https://api.venmo.com/v1/payments"
        #cd = os.path.dirname(os.path.abspath(__file__))
        #fn = os.path.join(cd, './venmo.keys')
        #with open(fn) as f:
            #self.__ApiKey__ = json.load(f)['sharang']
        #if not self.__ApiKey__:
            #raise('Api Key Error')

    def pay(self, payer_key, phone, note, amount):

        if amount > 20:
            print "You definitely didnt mean to pay $20"
            return

        params = {
            'access_token' : payer_key,
            'phone' : phone,
            'note' : note,
            'amount' : amount
            }

        try:
            data = urllib.urlencode(params)
            req = urllib2.Request(self.__paymentUrl__, data)
            response = urllib2.urlopen(req)
            result = response.read()
            print result
            return result
        except urllib2.URLError, e:
            print e

