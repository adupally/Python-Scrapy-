
    # scrapy crawl Amazon_Scrapy -o quotes.csv
    
import scrapy
import csv

class AmazonScrapy(scrapy.Spider):
   
    name = 'Amazon_Scrapy'
    
    
    start_urls = ['https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1']

    def parse(self, response):
         
        # Using this function to  make prices and no of reviews to number from string Because it contains "," which makes them string    
        def removecomma(s):
            if s is None:
                return s
            return s.replace(",","") 
        
            
        # Extract product details from the listing page 
        product_details = response.css('div.s-main-slot div.s-asin') 

        for product in product_details:
            rating = product.css('span.a-icon-alt::text').get()
            reviews = product.css('span.a-size-base::text').get()
            prices =product.css('span.a-price-whole::text').get()
            prices = removecomma(prices)
            reviews = removecomma(reviews)
            item = {
                'Product Name': product.css('span.a-text-normal::text').get(),
                'Product Price': prices,
                'Rating':  rating[0:3] if rating else "0.0",
                'Number of Reviews': reviews if reviews and reviews.isdigit() else "0" ,
                'Product URL': response.urljoin(product.css('a.a-link-normal::attr(href)').get())
            }
            yield item
            

        # Follow pagination links to scrape multiple pages
        # Pagination is Dynamic it will scrape all the data from  all pages till End.
        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()
        # print(next_page)
        if next_page:
            next_page = 'https://www.amazon.in'+ next_page
            # print(next_page)
            yield response.follow(next_page, callback=self.parse)




