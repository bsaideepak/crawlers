__author__ = 'Sai'


# Places API key: z6qpkrytcnydjwcnqu7wcar3

# /FindBusiness/?pg={page}&what={what}&where={where}&pgLen={page length}&lang={en|fr}&fmt={json|xml}&sflag={search flags}&apikey={xxxxxxxxxxxxxxxxxxxxxxxx}&UID={unique identifier}
# This module returns business details from the Yellow Pages "Places" API
# See YellowAPI docs for API details -- http://www.yellowapi.com/docs/places/

import urllib
import re
import xml.etree.ElementTree as ET
import time


class YellowAPI:

    def __init__(self):
        self.what = "restaurant" #str(what)
        self.city = "San-Jose"  #str(city)
        self.prov = "California"   #str(prov)
        self.pglen = 50
        self.uid = "50.156.90.215"
        self.apikey = "z6qpkrytcnydjwcnqu7wcar3"    #str(apikey)
        self.root = None


    def find_businesses(self):

        # build url for the YellowAPI in sandox format, returns xml by default.
        req = 'http://api.sandbox.yellowapi.com/FindBusiness/?what='+self.what+'&where='+ self.city + '&pgLen=' + str(self.pglen) + '&UID=50.156.90.215&apikey=z6qpkrytcnydjwcnqu7wcar3'
        response = urllib.urlopen(req)
        print("")
        print("")
        print("")
        print(response)
        print("")
        print("")
        print("")
        tree = ET.parse(response)
        print("")
        print(tree)
        print("")
        print("")
        self.root = tree.getiterator('Listing')
        print("")
        print("")

    def get_business_details(self):

        businessdetails = list()

        for listing in self.root:

            time.sleep(1)  # API doesn't allow more than 1 call per second in sandbox env, email for higher limit

            # replace all non-alphanumeric chars with '-' as required by API spec

            listingname = re.sub('[^0-9a-zA-Z]+', '-', listing[0].text)

            print(listingname)

            listingid = listing.get('id')

            print("")
            print(listingid)
            print("")

            print("Restaurant Not Found.")
            print("")

            if (listingname == "Peanuts-Deluxe-Cafe"):

                print("Restaurant Found.")

                province = re.sub('[^0-9a-zA-Z]+', '-', self.prov)
                city = re.sub('[^0-9a-zA-Z]+', '-', self.city)
                # now call to the API to get business details
                req2 = 'http://api.sandbox.yellowapi.com/GetBusinessDetails/?prov=' + province \
                   + '&city=' + city + '&bus-name=Peanuts-Deluxe-Cafe' + '&listingId=' + listingid \
                   + '&lang=en&fmt=xml&apikey=z6qpkrytcnydjwcnqu7wcar3&UID=50.156.90.215'
                response2 = urllib.urlopen(req2)
                tree2 = ET.parse(response2)

                # parse business details from element tree

                name = tree2.findtext('Name')
                street = tree2.findtext('Address/Street')
                city = tree2.findtext('Address/City')
                province = tree2.findtext('Address/Prov')
                postal = tree2.findtext('Address/Pcode')
                phones = tree2.findtext('Phones/Phone/DisplayNum')
                logo = tree2.findtext('Logos/Logo')
                url = tree2.findtext('Products/WebUrl')
                # more fields available, check API docs for details

                business = (name, street, city, province, postal, phones, logo, url)
                businessdetails.append(business)
                return businessdetails


def main():
    yellow = YellowAPI()
    yellow.find_businesses()
    businessdetails = yellow.get_business_details()
    print(businessdetails)

main()