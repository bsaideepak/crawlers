__author__ = 'Sai'

# CANCLED: ezlocal (not many listings), airyell (yext), switchboard (not good site), topix (articles + yelp listings), navmii (navigation app), opentable (too complex),

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
import sys
import re
import json


from template.items import YelpItem, ZomatoItem, LocalItem, BurrpItem, YelloBotItem, AmericanTownsItem, JustDialItem, CityGridItem, SuperPagesItem, IndiaMartItem, AllProductsItem, FoursquareItem, EveningflavoursItem, ZootoutItem, AsklailaItem, TimesCityItem, YellowPagesItem, ExportersIndiaItem, ThomasNetItem, PhoneNumberItem, PocketlyItem, HotfrogItem

from scrapy.http import Request

class YelpCrawlSpider(CrawlSpider):
    name = 'massBlurb_yelpSpider'

    def __init__(self,query, location, *args, **kwargs):
        global rules
        query = query.replace(' ','-')
        location = location.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/biz/'+query+'-'+ location+'')),callback='parse_item'),)
        self.allowed_domains = ['www.yelp.com']
        super(YelpCrawlSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]



    def parse_item(self,response):
        l = XPathItemLoader(item = YelpItem(),response = response)
        l.add_xpath('company','//*[@id="wrap"]/div[3]/div[1]/div/div[2]/div[1]/h1/text()')
        
        for i in range(1,8):
            
            l.add_xpath('day','//*[@id="super-container"]/div/div[1]/div[2]/div[2]/div[1]/table/tbody/tr['+str(i)+']/th[@scope="row"]/text()')
            l.add_xpath('timings1','//*[@id="super-container"]/div/div[1]/div[2]/div[2]/div[1]/table/tbody/tr['+str(i)+']/td[1]/span[1]/text()')
            l.add_xpath('timings2','//*[@id="super-container"]/div/div[1]/div[2]/div[2]/div[1]/table/tbody/tr['+str(i)+']/td[1]/span[2]/text()')
        return l.load_item()

#DONE.
#start-url="http://www.zomato.com/mumbai/restaurants?q=stomach"
#city="mumbai"
#query="stomach
#location="bandra"
#location1="west"
#area="plai hill"

#Requires input validation for area field. Not always necessary to be entered by the user. In such case, send '' as parameter since the spider needs it.

class ZomatoCrawlSpider(CrawlSpider):
    name = 'massBlurb_zomatoSpider'
    results = {}

    def __init__(self,city, location,location1,area, query, *args, **kwargs):
        global rules
        query = query.replace(' ','-')
        if area is not '':
            area = area.replace(' ','-')
            area = area+'-'
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'zomato.com/'+city+'/'+query+'-'+area+location+'-'+location1+'*'), deny=(r'/'+city+'/'+query+'-'+area+location+'-'+location1+'/menu*',r'/'+city+'/'+query+'-'+area+location+'-'+location1+'/map*',r'/'+city+'/'+query+'-'+area+location+'-'+location1+'/review*',r'/'+city+'/'+query+'-'+area+location+'-'+location1+'/info*',r'/'+city+'/'+query+'-'+area+location+'-'+location1+'/mulund-west-restaurant*',r'/'+city+'/'+query+'-'+area+location+'-'+location1+'/photo*')),callback='parse_item',follow=True),)
        print(location)
        print(query)
        print("##############")
        super(ZomatoCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.zomato.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(self.results)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@")

    def parse_item(self,response):
        l = XPathItemLoader(item = ZomatoItem(),response = response)

        l.add_xpath('phone1','//*[@id="phoneNoString"]/div/span/span[1]/text()')
        l.add_xpath('company','//html/body/div[3]/section/div/div[2]/div[2]/div[1]/h1/a/span/text()')
        l.add_xpath('phone2','//*[@id="phoneNoString"]/div/span/span[2]/text()')
        l.add_xpath('address','/html/body/div[3]/section/div/div[3]/div[3]/div[1]/div[2]/h4/text()[1]')
        l.add_xpath('review1','//*[@id="my-reviews-container"]/div[1]/div[3]/div[1]/div[1]/div[3]/div/div[1]/div/text()')
        l.add_xpath('review2','//*[@id="my-reviews-container"]/div[1]/div[3]/div[1]/div[2]/div[3]/div/div[1]/div/text()')
        l.add_xpath('timings','//*[@id="mainframe"]/section/div[1]/div/div[2]/div[1]/div[2]/div/div[4]/div[2]/div[1]/span/text()')

        res =  l.load_item()

        results = {'name':'','address':'','phone':'','review1':'','review2':'','timings':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'address' in res:
            results['address'] = res['address']
        if 'phone' in res:
            results['phone'] = res['phone']
        if 'review1' in res:
            results['review1'] = res['review1']
        if 'review2' in res:
            results['review2'] = res['review2']
        if 'timings' in res:
            results['timings'] = res['timings']

        return res


#Local DONE.
#input examples:-
#location="san jose ca"
#query="fahrenheit restaurant and lounge"
#start_url="http://www.local.com/business/results/location/query/"

class LocalCrawlSpider(CrawlSpider):
    name = 'massBlurb_localSpider'

    def __init__(self,location,query,state, *args, **kwargs):
        global rules
        query = query.replace(' ','-')
        location = location.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/business/details/'+location+'-'+state+'/'+query+'*')),callback='parse_item',follow=True),)
        super(LocalCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.local.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    #location is hard coded.
    #start_urls = ['http://www.local.com/business/results/?keyword='+query+'&location=San%20Jose%2C%20CA']

    def parse_item(self,response):
        l = XPathItemLoader(item = LocalItem(),response = response)

        l.add_xpath('company','//*[@id="biz-vcard"]/div[2]/h1/span/text()')
        l.add_xpath('phone','//*[@id="biz-vcard"]/div[5]/div[2]/address/p/strong/text()')
        l.add_xpath('locality','//*[@id="biz-vcard"]/div[5]/div[2]/address/p/span[2]/text()')
        l.add_xpath('region','//*[@id="biz-vcard"]/div[5]/div[2]/address/p/span[3]/text()')
        l.add_xpath('postalcode','//*[@id="biz-vcard"]/div[5]/div[2]/address/p/span[4]/text()')

        res =  l.load_item()

        results = {'name':'','address':'','phone':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'locality' in res:
            results['address'] = res['locality']
        if 'region' in res:
            results['address'] = results['address'] + res['region']
        if 'postalcode' in res:
            results['address'] = results['address'] + res['postalcode']
        if 'phone' in res:
            results['phone'] = results['phone']

        return res

#DONE.
#Input: location="locaity in the city, separated by -, if spaces exists in name. query="name of the restaurant. - for each space.""
# start_url="search url" --> start_url="http://www.burrp.com/mumbai/search.html?q=pop%20tates"

class BurrpCrawlSpider(CrawlSpider):
    name = 'massBlurb_burrpSpider'

    #replace spaces with - in query and location, while passing as parameter.
    #replace spaces with %20 while passing start_url as parameter.

    def __init__(self,query,location,area, *args, **kwargs):
        global rules
        query = query.replace(' ','-')
        location = location.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/'+location+'/'+query+'-'+area+'*')),callback='parse_item',follow=True),)
        super(BurrpCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.burrp.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):
        l = XPathItemLoader(item = BurrpItem(),response = response)

        l.add_xpath('company','//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/span/p/text()')
        l.add_xpath('phone','//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/div/ul/li[1]/strong/text()')
        l.add_xpath('address','//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/div/ul/li[2]/text()')
        l.add_xpath('region','//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/p/a/text()')
        l.add_xpath('cuisine1','//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/div/ul/li[3]/a[1]/text()')
        l.add_xpath('cuisine2','//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/div/ul/li[3]/a[2]/text()')

        res = l.load_item()

        results = {'name':'','address':'','phone':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'address' in res:
            results['address'] = res['address']
        if 'locality' in res:
            results['address'] = results['address'] + res['locality']
        if 'region' in res:
            results['address'] = results['address'] + res['region']
        if 'postalcode' in res:
            results['address'] = results['address'] + res['postalcode']

        return res

#DONE Perfectly.
#start_url =
# http://www.yellowbot.com/search?lat=&long=&q=peanuts+deluxe+cafe&place=san+jose



class YellowBotCrawlSpider(CrawlSpider):

    name = 'massBlurb_yellowbotSpider'

    def __init__(self,query,location,state, *args, **kwargs):
        global rules
        query = query.replace(' ','-')
        location = location.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=('/'+query+'-'+location+'-'+state+'*')), callback='parse_item',follow = True),)
        super(YellowBotCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.yellowbot.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item=YelloBotItem(),response=response)
        l.add_xpath('company','//*[@id="info-container"]/div[1]/h1/text()')
        l.add_xpath('street_address','//*[@id="info-container"]/div[1]/dl/dd[1]/span[1]/text()')
        l.add_xpath('locality','//*[@id="info-container"]/div[1]/dl/dd[1]/span[2]/text()')
        l.add_xpath('region','//*[@id="info-container"]/div[1]/dl/dd[1]/span[3]/text()')
        l.add_xpath('postalcode','//*[@id="info-container"]/div[1]/dl/dd[1]/span[4]/text()')


        res = l.load_item()

        results = {'name':'','address':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'street_address' in res:
            results['address'] = res['street_address']
        if 'locality' in res:
            results['address'] = results['address'] + res['locality']
        if 'region' in res:
            results['address'] = results['address'] + res['region']
        if 'postalcode' in res:
            results['address'] = results['address'] + res['postalcode']

        return res

#DONE.
#American Towns
#start_url="http://www.americantowns.com/ca/sanjose/search?searchtext=fahrenheit+restaurant&s_business=1&s_places=1&s_news=1&s_events=1"
#state="ca"  ---> two letter state initials
#city="name" --->sanjose

class AmericanTownsCrawlSpider(CrawlSpider):

    name = 'massBlurb_americantownsSpider'

    def __init__(self,state,city, *args, **kwargs):
        global rules
        self.rules = (Rule(SgmlLinkExtractor(allow=('/'+state+'/'+city+'/'+'yp/listing/sp-*')), callback='parse_item',follow = True),)
        super(AmericanTownsCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.americantowns.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = AmericanTownsItem(),response = response)
        l.add_xpath('company','//*[@id="sp_detail"]/div[1]/h1/text()')
        l.add_xpath('street_address','//*[@id="sp_detail"]/div[3]/div[1]/div/div[1]/text()')
        l.add_xpath('city','//*[@id="sp_detail"]/div[3]/div[1]/div/div[2]/text()')
        l.add_xpath('phone','//*[@id="sp_detail"]/div[3]/div[2]/text()')


        res = l.load_item()

        results = {'name':'','address':'','phone':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'street_address' in res:
            results['address'] = res['street_address']
        if 'city' in res:
            results['address'] = results['address'] + res['city']
        if 'phone' in res:
            results['address'] = results['address'] + res['phone']


        return res

#DONE.
#JustDial US
#start_url="http://us.justdial.com/CA/San_Jose/fahrenheit_restaurant/Downtown_San_Jose"
#state="CA" ---> two letter initials
#city="San_Jose"   ---> name
#query="Fahrenheit_Restaurant_And_Lounge"  ---> business_name --> Initials Capital. MUST.

#Landing url: http://us.justdial.com/CA/San_Jose/Peanuts_Deluxe_Cafe/near_7th_St,san_Fernando_St/BBL0076697-U2FuIEpvc2UsQ0EgcGVhbnV0cyBkZWx1eGUgY2FmZSBTQU4gSk9TRSBBVkU=


class JustDialUSCrawlSpider(CrawlSpider):

    name = 'massBlurb_justdialUSSpider'

    def __init__(self,state,city,query, *args, **kwargs):
        global rules
        city = city.replace(' ','_')
        query = query.replace(' ','_')
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/'+state+'/'+city+'/'+query+'/*')), callback='parse_item',follow = True),)
        super(JustDialUSCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['us.justdial.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = JustDialItem(),response = response)
        l.add_xpath('company','//*[@id="compdetails"]/section[1]/div/h1/span[1]/span/text()')
        l.add_xpath('address','/html/body/section[1]/section[3]/section[2]/section[2]/section[1]/section[1]/section[1]/dl[1]/dt[2]/text()')
        l.add_xpath('phone','//*[@id="compdetails"]/section[2]/span[2]/text()')

        res = l.load_item()

        results = {'name':'','address':'','phone':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'address' in res:
            results['address'] = res['address']
        if 'phone' in res:
            results['phone'] = res['phone']

        return res


#DONE BUT TOO MANY RESULTS.
#JustDial India
#start_url="http://www.justdial.com/Mumbai/pop-tates"
#city="Mumbai"   ---> name --> Initials Capital
#query="Pop-Tates"  ---> business_name --> Initials Capital. MUST.
#locality=""


class JustDialIndiaCrawlSpider(CrawlSpider):

    name = 'massBlurb_justdialIndiaSpider'

    def __init__(self,city,query, *args, **kwargs):
        global rules
        city = city.replace(' ','-')
        query = query.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/'+city+'/'+query+'*')), callback='parse_item',follow = True),)
        super(JustDialIndiaCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.justdial.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = JustDialItem(),response = response)
        l.add_xpath('company','/html/body/section[1]/section[4]/div/section[1]/section[1]/aside/h1/span/span/text()')
        l.add_xpath('address','/html/body/section[1]/section[4]/div/section[1]/section[2]/section[2]/section[1]/aside/p[2]/span[2]/span/text()')
        l.add_xpath('phone','/html/body/section[1]/section[4]/div/section[1]/section[2]/section[2]/section[1]/aside/p[1]/span[2]/a/text()')

        res = l.load_item()

        results = {'name':'','address':'','phone':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'address' in res:
            results['address'] = res['address']
        if 'phone' in res:
            results['phone'] = res['phone']

        return res


#DONE. But Pointless. Extra Zipcode Input required. End result is the name of the listing alone.
#CityGrid.
#start_url="http://www.citygrid.com/places/search?what=peanuts+deluxe+cafe&where=95112"
#take pincode also as input, for the start_url.
#take city also as input

class CityGridCrawlSpider(CrawlSpider):

    name = 'massBlurb_citygridSpider'

    def __init__(self,query,city, *args, **kwargs):
        global rules
        query = query.replace(' ','-')
        city = city.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=('/'+query+'-'+city)), callback='parse_item',follow = True),)
        super(CityGridCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.citygrid.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = CityGridItem(),response = response)
        l.add_xpath('company','//*[@id="place_header"]/div[2]/h2/text()')
        l.add_xpath('address','//*[@id="place_header"]/div[2]/p/span[1]/br/text()')
        l.add_xpath('phone','//*[@id="place_header"]/div[2]/p[2]/span[2]/text()')

        res =  l.load_item()

        results = {'name':'','address':'','phone':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'address' in res:
            results['address'] = res['address']
        if 'phone' in res:
            results['phone'] = res['phone']

        return res

# FILTERED OFFSITE REQUEST.
#SuperPages
#start_url=
# http://yellowpages.superpages.com/listings.jsp?CS=L&MCBP=true&C=peanuts+deluxe+cafe%2C+san+jose+ca&STYPE=S&search=Find+It&submit=Search
#limit=
# http://www.superpages.com/bp/San-Jose-CA/Peanuts-Deluxe-Cafe-L0020274184.htm?C=peanuts+deluxe+cafe%2C+san+jose+ca&lbp=1&STYPE=S&TR=77&bidType=FLCLIK&PGID=yp609.8083.1405754605752.1951281190764&dls=true&bpp=1
#query="Peanuts-Deluxe-Cafe"
#location="San-Jose-CA"

class SuperPagesCrawlSpider(CrawlSpider):

    name = 'massBlurb_superpagesSpider'

    def __init__(self, location, query, *args, **kwargs):
        global rules
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/bp/'+location+'/'+query+'*')), callback='parse_item',follow = True),)
        super(SuperPagesCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['wwww.superpages.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = SuperPagesItem(),response = response)
        l.add_xpath('company','//*[@id="coreBizName_nonad"]/h1/text()')
        l.add_xpath('address','//*[@id="coreBizAddress"]/text()')
        l.add_xpath('phone','//*[@id="phNos"]/span/text()')

        res =  l.load_item()

        results = {'name':'','address':'','phone':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'address' in res:
            results['address'] = res['address']
        if 'phone' in res:
            results['phone'] = res['phone']

        return results


#DONE.
#IndiaMart
#start_url="http://dir.indiamart.com/cgi/catprdsearch.mp?ss=khandela+electronika"
#query="khandela-electronika"

class IndiaMartCrawlSpider(CrawlSpider):

    name = 'massBlurb_indiamartSpider'

    def __init__(self,query, *args, **kwargs):
        global rules
        query = query.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=('/'+query+'*')), callback='parse_item',follow = True),)
        super(IndiaMartCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.indiamart.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = IndiaMartItem(),response = response)
        l.add_xpath('company','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/span[3]/h1/text()')
        l.add_xpath('street_address','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/div[3]/span[1]/text()')
        l.add_xpath('locality','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/div[3]/span[2]/text()')
        l.add_xpath('region','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/div[3]/span[4]/text()')
        l.add_xpath('postalcode','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/div[3]/span[3]/text()')
        l.add_xpath('phone','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/span[5]/text()')

        res =  l.load_item()

        return res


#DONE. But results are not complete. Recheck.
#AllProducts
#start_url="http://www.allproducts.com/search2/search.php?query=Lightvision+technologies&kind=supplier&Search.x=0&Search.y=0"
#category="light"
#query="lightvision"


class AllProductsCrawlSpider(CrawlSpider):

    name = 'massBlurb_allproductsSpider'

    def __init__(self,category, query, *args, **kwargs):
        global rules
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/'+category+'/'+query),deny=(r'/'+category+'/'+query+'/\d+',r'/'+category+'/'+query+'/showroom*')), callback='parse_item',follow = True),)
        super(AllProductsCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.allproducts.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = AllProductsItem(),response = response)
        l.add_xpath('company','//*[@id="main"]/div[3]/div/strong/text()')
        l.add_xpath('address','//*[@id="main"]/div[2]/div[2]/div[3]/span[2]/text()')
        l.add_xpath('sales_contact','//*[@id="main"]/div[2]/div[2]/div[2]/span[2]/text()')
        l.add_xpath('phone','//*[@id="main"]/div[2]/div[2]/div[4]/span[2]/text()')
        l.add_xpath('company_profile','//*[@id="aupd"]/tbody/tr/td/div/p/text()')
        l.add_xpath('year_of_establishment','//*[@id="main"]/div[2]/div[1]/div[2]/span[2]/text()')
        l.add_xpath('capital','//*[@id="main"]/div[2]/div[1]/div[3]/span[2]/text()')
        l.add_xpath('annual_sales','//*[@id="main"]/div[2]/div[1]/div[4]/span[2]/text()')
        l.add_xpath('markets','//*[@id="main"]/div[2]/div[1]/div[7]/span[2]/ul/li[1]/text()')
        l.add_xpath('url','//*[@id="main"]/div[2]/div[2]/div[7]/span[2]/a[1]/text()')
        l.add_xpath('email','//*[@id="main"]/div[2]/div[2]/div[6]/span[2]/a/text()')

        res=  l.load_item()

        results = {'name':'','address':'','phone':'','sales_contact':'','annual_sales':'','capital':'','year_of_establishment':'','company_profile':'','markets':'','url':'','email':''}

        return res

#DONE.
#Foursquare
#start_url="https://foursquare.com/explore?mode=url&near=San%20Jose&q=peanuts%20deluxe%20cafe"
#queries need to be as exact as possible.


class FoursquareCrawlSpider(CrawlSpider):
    name = 'massBlurb_foursquareSpider'

    def __init__(self, query, *args, **kwargs):
        global rules
        query = query.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/v/'+query+'/*')),callback='parse_item'),)
        super(FoursquareCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['foursquare.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):
        l = XPathItemLoader(item = FoursquareItem(),response = response)

        l.add_xpath('phone','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/span/text()')
        l.add_xpath('st_add','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/span[1]/text()')
        l.add_xpath('locality','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/span[2]/text()')
        l.add_xpath('state','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/span[3]/text()')
        l.add_xpath('postalcode','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/span[4]/text()')
        l.add_xpath('country','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/text()[3]/text()')
        l.add_xpath('company','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/h1/text()')

        res =  l.load_item()
        results = {'name':'','address':'','phone':'','timings':''}


        if 'company' in res:
            results['name'] = res['company']
        if 'st_add' in res:
            results['address'] = res['st_add']
        if 'locality' in res:
            results['address'] = results['address'] + res['locality']
        if 'state' in res:
            results['address'] = results['address'] + res['state']
        if 'postalcode' in res:
            results['address'] = results['address'] + res['postalcode']
        if 'country' in res:
            results['address'] = results['address'] + res['country']
        if 'phone' in res:
            results['phone'] = res['phone']

        return results


# REQUEST BEING FILTERED.
#EveningFlavours
#start_url=
# http://eveningflavors.com/Restaurants-Pubs-GenericSearch-Process/Restaurants-Pubs-Hotels-Lounge-Search-India.jsp?city=Mumbai&checkRequestPage=quickSearch&inputForQuickSearch=stomach&placeLookingInput=bandra+west
#limit=
# http://eveningflavors.com/Stomach/Mumbai/6747/

class EveningFlavoursCrawlSpider(CrawlSpider):
    name = 'massBlurb_eveningflavoursSpider'

    def __init__(self, location, query, *args, **kwargs):
        global rules
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/'+query+'/'+location+'/*')), callback='parse_item',follow = True),)
        super(EveningFlavoursCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.eveningflavours.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):
        l = XPathItemLoader(item = EveningflavoursItem(),response = response)
        l.add_xpath('phone','//*[@id="Prof-Quickview-Desc"]/p/text()')
        l.add_xpath('address','//*[@id="profiletab1"]/p/font/text()')
        l.add_xpath('timings','//*[@id="Prof-Quickview-Heading"]/p/font/b')
        l.add_xpath('company','//*[@id="table48"]/tbody/tr[2]/td[1]/h1/span/a/text()')

        res =  l.load_item()
        results = {'name':'','address':'','phone':'','timings':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'address' in res:
            results['address'] = res['address']
        if 'phone' in res:
            results['phone'] = res['phone']
        if 'timings' in res:
            results['timings'] = res['timings']

        return res


#Done. Perfectly.
#Zootout
#start_url="http://www.zootout.com/mumbai/stomach-bandra-west-4162"
#location="mumbai"

class ZootoutCrawlSpider(CrawlSpider):

    name = 'massBlurb_zootoutSpider'

    def __init__(self,query,location, *args, **kwargs):
        global rules
        location = location.replace(' ','-')
        query = query.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=('/'+query+'-'+location+'*')), callback='parse_item',follow = True),)
        super(ZootoutCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.zootout.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = ZootoutItem(),response = response)
        l.add_xpath('company','/html/body/div[5]/div[1]/div/div[2]/div[1]/h1/span/text()')
        l.add_xpath('st_add','//*[@id="port"]/div/div[1]/div/div[1]/div/text()')
        l.add_xpath('locality','//*[@id="port"]/div/div[1]/div/div[1]/a/text()')
        l.add_xpath('timings','//*[@id="port"]/div/div[1]/div/div[11]/text()')
        l.add_xpath('phone','/html/body/div[5]/div[1]/div/div[2]/div[1]/div[3]/span[2]/text()')

        res =  l.load_item()
        print("")
        results = {'name':'','address':'','phone':'','timings':''}
        print("Printing from results")
        if 'company' in res:
            results['name'] = res['company']
        if 'st_add' in res:
            results['address'] = res['st_add']
        if 'locality' in res:
            results['address'] = results['address'] + res['locality']
        if 'phone' in res:
            results['phone'] = res['phone']
        if 'timings' in res:
            results['timings'] = res['timings']
        return results


#DONE. ----------TEST--------------
#Asklaila
#User Input: location= "Bandra", location1="West" , city="Mumbai" , q = "stomach"
#start_url="http://www.asklaila.com/search/Mumbai/bandra/stomach/?searchNearby=true"
#limit: "http://www.asklaila.com/listing/Mumbai/Bandra+West/Stomach/1dHGIAZT/"

class AsklailaCrawlSpider(CrawlSpider):

    name = 'massBlurb_asklailaSpider'

    def __init__(self,city,location, location1, q, *args, **kwargs):
        global rules
        loc = location.replace(' ','+')
        print('/listing/'+city+'/'+loc+'+'+location1+'/'+q+'/*')
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/listing/'+city+'/'+location+'.'+location1+'/'+q+'/*')), callback='parse_item',follow = True),)
        print('/listing/'+city+'/'+loc+'+'+location1+'/'+q+'/*')
        super(AsklailaCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.asklaila.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = AsklailaItem(),response = response)
        l.add_xpath('company','//*[@id="all-content"]/div[4]/div[1]/div[1]/div[1]/div[1]/h1/span/text()')
        l.add_xpath('st_add','//*[@id="ldpAdrsDetails"]/p[2]/span/span[1]/text()')
        l.add_xpath('locality','//*[@id="ldpAdrsDetails"]/p[2]/span/span[2]/a/title/text()')
        l.add_xpath('region','//*[@id="ldpAdrsDetails"]/p[2]/span/span[3]/text()')
        l.add_xpath('postalcode','//*[@id="ldpAdrsDetails"]/p[2]/span/span[4]/text()')
        l.add_xpath('phone','//*[@id="ldpAdrsDetails"]/p[1]/span/span[1]/text()')

        res =  l.load_item()

        results = {'name':'','address':'','phone':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'st_add' in res:
            results['address'] = res['st_add']
        if 'locality' in res:
            results['address'] = results['address'] + res['locality']
        if 'region' in res:
            results['address'] = results['address'] + res['region']
        if 'postalcode' in res:
            results['address'] = results['address'] + res['postalcode']
        if 'phone' in res:
            results['phone'] = res['phone']

        return results

#DONE.
#Timescity
#start_url="http://timescity.com/mumbai/search?searchname=vihang%27s%20inn"
#limit: http://timescity.com/mumbai/thane-west/north-indian-restaurant-palm-court/73059

class TimesCityCrawlSpider(CrawlSpider):

    name = 'massBlurb_timescitySpider'

    def __init__(self, location, area, *args, **kwargs):
        global rules
        area = area.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/'+location+'/'+area+'/*')), callback='parse_item',follow = True),)
        super(TimesCityCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['timescity.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = TimesCityItem(),response = response)
        l.add_xpath('company','//*[@id="restaurantDetailDiv"]/div[1]/div/div[1]/div[1]/h1/a/url/text()')
        l.add_xpath('near','//*[@id="restaurantDetailDiv"]/div[2]/div/div[1]/div[1]/span[3]/span/text()')
        l.add_xpath('locality','//*[@id="restaurantDetailDiv"]/div[2]/div/div[1]/div[1]/span[2]/meta[1]/content/text()')
        l.add_xpath('region','//*[@id="info-container"]/div[1]/dl/dd[1]/span[3]/text()')
        l.add_xpath('postalcode','//*[@id="restaurantDetailDiv"]/div[2]/div/div[1]/div[1]/span[2]/meta[2]/text()')
        l.add_xpath('st_add','//*[@id="restaurantDetailDiv"]/div[2]/div/div[1]/div[1]/span[2]/meta[3]/content')

        res =  l.load_item()

        return res

#DONE. Perfectly.
#YellowPages
#start_url:
# http://www.yellowpages.com/san-jose-ca/peanuts-deluxe-cafe?g=san%20jose%2C%20ca&q=%20peanuts%20deluxe%20cafe


class YellowPagesCrawlSpider(CrawlSpider):

    name = 'massBlurb_ypSpider'

    def __init__(self,query,location, *args, **kwargs):
        global rules
        location = location.replace(' ','-')
        query = query.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=('/'+location+'/mip/'+query+'*')), callback='parse_item',follow = True),)
        super(YellowPagesCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.yellowpages.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = YellowPagesItem(),response = response)
        l.add_xpath('company','//*[@id="main-content"]/div[1]/div[1]/h1/text()')
        l.add_xpath('st_add','//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]/p[1]/text()')
        l.add_xpath('city','//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]/p[2]/text()')
        l.add_xpath('phone','//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]/p[3]/text()')

        #reviews left

        res =  l.load_item()
        print("")
        print("")
        results = {'name':'','address':'','phone':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'st_add' in res:
            results['address'] = res['st_add']
        if 'city' in res:
            results['address'] = results['address'] + res['city']
        if 'phone' in res:
            results['phone'] = res['phone']

        print("")
        return res


#DONE.
#PhonenNmber
#start_url:
# http://www.phonenumber.com/business?key=peanuts+deluxe+cafe&where=San+Jose%2C+CA


class PhoneNumberCrawlSpider(CrawlSpider):

    name = 'massBlurb_phonenumberSpider'

    def __init__(self,query,location, *args, **kwargs):
        global rules
        location = location.replace(' ','-')
        query = query.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=('/business/'+query+'-'+location)), callback='parse_item',follow = True),)
        super(PhoneNumberCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.phonenumber.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = PhoneNumberItem(),response = response)
        l.add_xpath('company','//*[@id="business_name"]/text()')
        l.add_xpath('street_address','//*[@id="left"]/div[1]/div[2]/div[3]/div[1]/div[1]/div/text()')
        l.add_xpath('locality','//*[@id="left"]/div[1]/div[2]/div[3]/div[1]/div[1]/span[1]/text()')
        l.add_xpath('region','//*[@id="left"]/div[1]/div[2]/div[3]/div[1]/div[1]/abbr/text()')
        l.add_xpath('postalcode','//*[@id="left"]/div[1]/div[2]/div[3]/div[1]/div[1]/span[2]/text()')
        #l.add_xpath('hours','//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]/p[2]/text()')
        l.add_xpath('phone','//*[@id="phones_list"]/span/span/text()')


        res =  l.load_item()
        print("")
        print("")
        return res


#Done.
#Pocketly
#start_url =
# http://pocketly.com/search?keywords=peanuts+deluxe+cafe&location=san+jose&longitude=&latitude=


class PocketlyCrawlSpider(CrawlSpider):

    name = 'massBlurb_pocketlySpider'

    def __init__(self,query,location, *args, **kwargs):
        global rules
        location = location.replace(' ','-')
        query = query.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=('/biz/'+query+'-'+location+'/*')), callback='parse_item',follow = True),)
        super(PocketlyCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['pocketly.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = PocketlyItem(),response = response)
        l.add_xpath('company','//*[@id="storeName"]/text()')
        l.add_xpath('street_address','//*[@id="address1"]/text()')
        l.add_xpath('city','//*[@id="addressCity"]/text()')
        l.add_xpath('state','//*[@id="addressState"]/text()')
        l.add_xpath('postalcode','//*[@id="addressZip"]/text()')
        l.add_xpath('phone','//*[@id="phoneNumber"]/text()')


        res =  l.load_item()
        print("")
        print("")
        return res
        print("")
        print("")


#DONE. Perfectly.
#exportersindia.com
#start_url:
# http://www.exportersindia.com/search.php?term=electronika&srch_catg_ty=comp
#limit:
# http://www.exportersindia.com/ptagiselectronika/


class ExportersIndiaCrawlSpider(CrawlSpider):

    name = 'massBlurb_exportersindiaSpider'

    def __init__(self,query, *args, **kwargs):
        global rules
        self.rules = (Rule(SgmlLinkExtractor(allow=('/'+query+'/*')), callback='parse_item',follow = True),)
        super(ExportersIndiaCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['exportersindia.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = ExportersIndiaItem(),response = response)
        l.add_xpath('company','//*[@id="logo"]/section/ul/li/h1/text()')
        l.add_xpath('company_info','//*[@id="wideColumn"]/section[1]/nav/p/text()')
        l.add_xpath('contact_person','//*[@id="thinColumn"]/section[2]/nav/b/text()')
        l.add_xpath('address','//*[@id="thinColumn"]/section[2]/nav/p[1]/text()')
        l.add_xpath('phone','//*[@id="thinColumn"]/section[2]/nav/p[2]/text()')
        l.add_xpath('fax','//*[@id="thinColumn"]/section[2]/nav/p[3]/text()')
        l.add_xpath('business_type','//*[@id="wideColumn"]/section[2]/nav/p[1]/span[3]/text()')
        l.add_xpath('company_turnover','//*[@id="wideColumn"]/section[2]/nav/p[3]/span[3]/text()')
        l.add_xpath('markets','//*[@id="wideColumn"]/section[2]/nav/p[4]/span[3]/text()')

        print("")
        res =  l.load_item()

        results = {'company':'','company_info':'','address':'','phone':'','contact_person':'','fax':'','business_type':'','company_turnover':'','markets':''}

        if 'company' in res:
            results['name'] = res['company']
        if 'company_info' in res:
            results['company_info'] = res['company_info']
        if 'address' in res:
            results['address'] = res['address']
        if 'phone' in res:
            results['phone'] = res['phone']
        if 'contact_person' in res:
            results['contact_person'] = res['contact_person']
        if 'fax' in res:
            results['fax'] = res['fax']
        if 'business_type' in res:
            results['business_type'] = res['business_type']
        if 'company_turnover' in res:
            results['company_turnover'] = res['company_turnover']
        if 'markets' in res:
            results['markets'] = res['markets']

        print("")
        print(results)


#Thomasnet.com
#start_url:
# http://www.thomasnet.com/search.html?which=all&WTZO=Find+Suppliers&searchx=true&what=electronika&Submit.x=0&Submit.y=0&Submit=Search


class ThomasNetCrawlSpider(CrawlSpider):

    name = 'massBlurb_thomasnetSpider'

    def __init__(self,*args, **kwargs):
        global rules
        self.rules = (Rule(SgmlLinkExtractor(allow=(r'/profile/*')), callback='parse_item',follow = True),)
        super(ThomasNetCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['thomasnet.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):
        print("Hi")

        l = XPathItemLoader(item = ThomasNetItem(),response = response)
        l.add_xpath('company','//*[@id="profilehead"]/tbody/tr[1]/td/h1/a/text()')
        l.add_xpath('company_profile','//*[@id="coprobody"]/b/text()/br[1]/text()')
        #l.add_xpath('phone','//*[@id="phones-30121314"]/strong[1]]/text()')
        #l.add_xpath('fax','//*[@id="phones-30121314"]/text()')

        res =  l.load_item()

        print("")
        print(res)
        print("")


#DONE.
#Hotfrog.
#start_url=
#  http://www.hotfrog.com/Products/Peanuts/CA/San-Jose
#limit:
#  http://www.hotfrog.com/Companies/Peanuts-Deluxe-Cafe

class HotfrogCrawlSpider(CrawlSpider):

    name = 'massBlurb_hotfrogSpider'

    def __init__(self,query, *args, **kwargs):
        global rules

        query = query.replace(' ','-')
        self.rules = (Rule(SgmlLinkExtractor(allow=('/Companies/'+query)), callback='parse_item',follow = True),)


        super(HotfrogCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['www.hotfrog.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = HotfrogItem(),response = response)
        l.add_xpath('company','//*[@id="content"]/div[2]/div[1]/h1/text()')
        l.add_xpath('address','//*[@id="content"]/div[2]/div[4]/text()[1]')
        l.add_xpath('phone','//*[@id="content"]/div[2]/div[4]/text()[2]')


        res =  l.load_item()
        print("")
        print("")
        return res
        print("")
        print("")


#Done. Check json file generated. If the file is non empty, there exist company/companies with the searched name..
#ecplaza.net
#start_url:
# http://www.ecplaza.net/tamo--company.html

class ECPlazaCrawlSpider(CrawlSpider):

    name = 'massBlurb_ecplazaSpider'

    def __init__(self,*args, **kwargs):
        global rules
        self.rules = (Rule(SgmlLinkExtractor(allow=('en.ecplaza.net')), callback='parse_item',follow = True),)
        super(ECPlazaCrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['ecplaza.net']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = HotfrogItem(),response = response)
        l.add_xpath('company','/html/body/div[3]/div[1]/table[1]/text()')
        res =  l.load_item()
        print("")
        print("")
        return res
        print("")
        print("")


#Done. Check json file generated. If the file is non empty, there exist company/companies with the searched name..
#ec21
#start_url:
# http://supplier.ec21.com/tamo_technology_co_ltd.html

class EC21CrawlSpider(CrawlSpider):

    name = 'massBlurb_ec21Spider'

    def __init__(self,*args, **kwargs):
        global rules
        self.rules = (Rule(SgmlLinkExtractor('en.ec21.com'), callback='parse_item',follow = True),)
        super(EC21CrawlSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['ec21.com']
        self.start_urls = [kwargs.get('start_url')]
        print(self.start_urls)

    def parse_item(self,response):

        l = XPathItemLoader(item = HotfrogItem(),response = response)
        l.add_xpath('company','/html/body/center/table[2]/text()')
        res =  l.load_item()
        print("")
        print("")
        return res
        print("")
        print("")