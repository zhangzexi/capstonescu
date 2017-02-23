import zillow_web_scraper_client as client
import csv

with open('eggs.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

ZIPCODE_FILE = '/Users/zhoutaozhang/Downloads/SmartZillow-master/data_fetcher/bay_area_zipcode.txt'

zipcode_list = []

with open(ZIPCODE_FILE, 'r') as zipcode_file:
    for zipcode in zipcode_file:
        zipcode_list.append(str(zipcode))

f = open('/Users/zhoutaozhang/Desktop/bay_area1.txt', 'w')
counter = 0
for zipcode in zipcode_list:
    for x in range(1,21):
        for i in  client.get_properties_by_zip(str(zipcode) + '/'+ str(x) +'_p/'):
            counter += 1
            f.write(str(counter) + '.' +str(i) + '\n')

