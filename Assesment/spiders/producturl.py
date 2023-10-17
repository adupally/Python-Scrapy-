import scrapy
import csv

class producturl(scrapy.Spider):
    
    name = 'producturl'
    allowed_domains = ['amazon.in']
    def start_requests(self):
        
        # OPENING THE OUTPUT FILE OF AMAZON_SCRAPY AND TAKING URL FROM IT.
        with open('output.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield scrapy.Request(url=row['Product URL'], callback=self.parse)

    def parse(self, response):
        
        # To extract the manufaturer name from the product details
        def extract_manufacturer_from_location(potential_locations):
            for location_selector in potential_locations:
                data = response.css(location_selector).get()
                if data and is_likely_manufacturer(data):
                    data=data.split(":")
                    return data[1]
            return None

        # Checking whether there is manufacturer in the product details
        def is_likely_manufacturer(data):
            keyword = "manufacturer"
            if keyword in data.lower():
                return True
            return False
        # The manufacturer name is in different locations in different links so that to check in which path is it there
        potential_locations=[
            'div#detailBullets_feature_div ul li:nth-child(3) ::text',
            'div#detailBullets_feature_div ul li:nth-child(4) ::text',
                            ]
        
        
        # Calling the function to check wheather there is manufacture
        manufacturer = extract_manufacturer_from_location(potential_locations)
        
        
        # If manufacturer name is not there in product details 
        # In some Url there will not be product details but there will be techincal details Table 
        if manufacturer is None:
            tech_spec_table = response.css('div#productDetails_techSpec_section_1 table tbody tr')
            for tr in tech_spec_table:
                th = tr.css('th::text').get()
                if th and "manufacturer" in th.strip().lower():
                    manufacturer = tr.css('td::text').get()
                    
                    
        # if manufacturer name is not present in the product details and techincal details table then checks for the store which present near the product price
        # why i am doing this check at last because in some Url here there is a store link or brand but manufacturer is different in product details 
        # So if there no manufacturer details in above it will take from here
        if manufacturer is None:
            manufacturer = response.css('a#bylineInfo::text').get()
            if manufacturer:
                if manufacturer.startswith("Visit"):
                    manufacturer=manufacturer.split(" ")
                    manufacturer = manufacturer[2:-1]
                else:
                    manufacturer=manufacturer.split(":")
                    manufacturer=manufacturer[1]
                    
        
        Description=response.css('#feature-bullets ul li span::text').getall()
        Asin = response.url.split('/')[-1]
        
        if Asin.startswith("ref"):
            Asin=""
        product_Description = response.css('#productDescription p span::text').get()
        
        item = {
            'Description': Description if Description else "None",
            'ASIN': Asin if Asin else "None",
            'Product Description': product_Description if product_Description  else "None",
            'Manufacturer': manufacturer if manufacturer else "None"
        }
        yield item
