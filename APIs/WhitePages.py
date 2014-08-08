__author__ = 'Sai'

# API Keys: 658602f30bc7c402cda256632cac6c7f
# Request format: https://proapi.whitepages.com/2.0/business.json?name=toyota&city=Seattle&api_key=KEYVAL

import sys
import requests


class WhitePages:

    name = sys.argv[1]
    city = sys.argv[2]
    state_code = sys.argv[3]

    def businessSearch(self):

        if(self.state_code is not None and self.city is not None and self.name is not None):

            req = "https://proapi.whitepages.com/2.0/business.json?name="+self.name+"&city="+self.city+"&state_code="+self.state_code+"&api_key=658602f30bc7c402cda256632cac6c7f"
            res = requests.get(req)

            #print(res.text)
            print("")
            response =  res.json()

            key1 = ''.join(str(response['results'][0]))
            name = response['dictionary'][key1]['name']
            key2 = ''.join(str(response['dictionary'][key1]['locations'][0]['id']['key']))
            address1 = response['dictionary'][key2]['standard_address_line1']
            address2 = response['dictionary'][key2]['standard_address_line2']
            location = response['dictionary'][key2]['standard_address_location']
            address = address1 + " " +address2 + " " +location
            key3 = response['dictionary'][key1]['phones'][0]['id']['key']
            phone = response['dictionary'][key3]['phone_number']
            results = {'name':name,'address':address,'phone':phone}

            print(results)

            print("")

x = WhitePages()
x.businessSearch()

