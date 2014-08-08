from scrapy.item import Item,Field

class YelpItem(Item):
    timings1 = Field()
    company = Field()
    address = Field()
    timings2 = Field()
    day = Field()

class ZomatoItem(Item):
    phone1 = Field()
    company = Field()
    address = Field()
    phone2 = Field()
    review1 = Field()
    review2 = Field()
    review3 = Field()
    timings = Field()

class LocalItem(Item):
    phone = Field()
    company = Field()
    locality = Field()
    region = Field()
    postalcode = Field()

class BurrpItem(Item):
    phone = Field()
    company = Field()
    region = Field()
    address = Field()
    cuisine1 = Field()
    cuisine2 = Field()

class YelloBotItem(Item):
    phone = Field()
    company = Field()
    locality = Field()
    region = Field()
    postalcode = Field()
    street_address = Field()

class SwitchBoardItem(Item):
    phone = Field()
    company = Field()
    locality = Field()
    region = Field()
    postalcode = Field()
    street_address = Field()
    timings = Field()

class EZLocalItem(Item):
    phone = Field()
    company = Field()
    locality = Field()
    region = Field()
    postalcode = Field()
    street_address = Field()

class AmericanTownsItem(Item):
    phone = Field()
    company = Field()
    city = Field()
    street_address = Field()

class JustDialItem(Item):
    phone = Field()
    company = Field()
    address = Field()

class CityGridItem(Item):
    phone = Field()
    company = Field()
    address = Field()

class SuperPagesItem(Item):
    phone = Field()
    company = Field()
    address = Field()

class IndiaMartItem(Item):
    phone = Field()
    company = Field()
    locality = Field()
    region = Field()
    postalcode = Field()
    street_address = Field()
    year_of_establishment = Field()
    nature_of_business = Field()
    company_profile = Field()

class AllProductsItem(Item):
    phone = Field()
    company = Field()
    sales_contact = Field()
    address = Field()
    year_of_establishment = Field()
    company_profile = Field()
    capital = Field()
    annual_sales = Field()
    number_of_employees = Field()
    business_type_1 = Field()
    business_type_2 = Field()
    markets = Field()
    url = Field()
    email = Field()

class FoursquareItem(Item):
    phone = Field()
    company = Field()
    locality = Field()
    region = Field()
    postalcode = Field()
    street_address = Field()
    state = Field()
    country = Field()

class EveningflavoursItem(Item):
    phone = Field()
    company = Field()
    address = Field()
    timings = Field()

class ZootoutItem(Item):
    phone = Field()
    company = Field()
    timings = Field()
    st_add = Field()
    locality = Field()

class AsklailaItem(Item):
    phone = Field()
    company = Field()
    timings = Field()
    st_add = Field()
    locality = Field()
    region = Field()
    postalcode = Field()

class TimesCityItem(Item):
    phone = Field()
    company = Field()
    locality = Field()
    region = Field()
    postalcode = Field()
    st_add = Field()
    near = Field()
class YellowPagesItem(Item):
    phone = Field()
    phone = Field()
    timings = Field()
    st_add = Field()
    city = Field()
    company = Field()

class ExportersIndiaItem(Item):
    phone = Field()
    company = Field()
    contact_person = Field()
    address = Field()
    year_of_establishment = Field()
    company_info = Field()
    business_type = Field()
    markets = Field()
    fax = Field()
    company_turnover = Field()

class temp(Item):
    name = Field()
    company_info = Field()
    address = Field()
    phone =Field()
    contact_person = Field()
    fax = Field()
    business_type = Field()
    company_turnover = Field()
    markets = Field()

class ThomasNetItem(Item):
    company = Field()
    address = Field()
    phone =Field()
    fax = Field()

class PhoneNumberItem(Item):
    company = Field()
    street_address = Field()
    locality = Field()
    region = Field()
    postalcode = Field()
    phone = Field()
    hours = Field()

class PocketlyItem(Item):
    company = Field()
    street_address = Field()
    state = Field()
    city = Field()
    postalcode = Field()
    phone = Field()

class HotfrogItem(Item):
    company = Field()
    address = Field()
    phone = Field()

class ECPlazaItem(Item):
    company = Field()
