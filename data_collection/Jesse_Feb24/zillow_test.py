import zillow_data as client
import csv
import pandas as pd

with open('eggs.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

ZIPCODE_FILE = 'C:\Users\Jesse\Desktop\zipdata.txt'
zipcode_list = []
with open(ZIPCODE_FILE, 'r') as zipcode_file:
    for zipcode in zipcode_file:
        zipcode_list.append(str(zipcode))

df = pd.DataFrame()
count = 0
for zip in zipcode_list:
    for x in range(1,21):
        for i in  client.get_properties_by_zip(str(zip) + '/'+ str(x) +'_p/'):
            print count
            count = count + 1
            df = pd.concat([df,client.ready_for_concat(i)])

df.to_csv('C:\Users\Jesse\Desktop\dataset.csv')
