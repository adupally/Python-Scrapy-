# Python-Scrapy-

Command to run :: scrapy crawl filename -o outputfilename.csv


In the Amazon_Scrapy.py file first we get the data of 
• Product Name
• Product Price 
• Rating
• Number of reviews
• Product URL

and stored it in the output.csv file.



In the producturl.py file we scrape the data of 
• Description
• ASIN
• Product Description
• Manufacturer

by taking the Product Url from the output.csv file and hit those urls in the producturl.py and scrapes the data and stores it in the output1.csv file.
