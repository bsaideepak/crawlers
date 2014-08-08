__author__ = 'Sai'

import subprocess
from subprocess import Popen, PIPE

#abc = subprocess.Popen('scrapy crawl massBlurb_ypSpider -a location="san-jose-ca" -a query="peanuts-deluxe-cafe" -a start_url="http://www.yellowpages.com/san-jose-ca/peanuts-deluxe-cafe?g=san%20jose%2C%20ca&q=%20peanuts%20deluxe%20cafe"', shell=True)


Popen(['scrapy crawl massBlurb_ypSpider -a location="san-jose-ca" -a query="peanuts-deluxe-cafe" -a start_url="http://www.yellowpages.com/san-jose-ca/peanuts-deluxe-cafe?g=san%20jose%2C%20ca&q=%20peanuts%20deluxe%20cafe"'], shell=True, stdout=PIPE).communicate()

#print(stdout)