import pandas as pd
from pymongo import MongoClient
pd.options.mode.chained_assignment = None

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017'
DB_NAME = 'real_estate_smart_view_testing'

client = MongoClient('%s:%s' % (MONGO_DB_HOST, MONGO_DB_PORT))

def getDB(db=DB_NAME):
    db = client[db]
    return db



def clean(df):
    mask = (
    (df.property_type != "Condo") & (df.property_type != "Single Family") & (df.property_type != "Multi Family") & (
    df.property_type != "Townhouse"))
    df = df[~mask]
    df = df[df.bedroom < 10]
    df = df[df.bathroom < 10]
    df = df[df.list_price > 0]
    df = df[df["size"] > 0]
    df = df[(df.bathroom != 0) & (df.bedroom != 0)]
    df.index = range(len(df))
    df["lotsize"] = getLot(df)
    df.drop(
        ["_id", "is_for_sale", "state", "street_address", "zipcode", "zpid", "description", "image_url", "last_update",
         "latitude", "longitude", "facts"], axis=1, inplace=True)

def getLot(df):
    lotsize = []
    for i in range(len(df["facts"])):
        count = 0
        for j in range(len(df["facts"][i])):
            if "Lot:" in df["facts"][i][j]:
                temp = df["facts"][i][j + 1].split()
                if temp[1] == "sqft":
                    res = temp[0].replace(",", "")
                    lotsize.append(int(res))
                if "acre" in temp[1]:
                    res = float(temp[0].replace(",", ""))
                    if res > 1000:
                        lotsize.append(res)
                    else:
                        lotsize.append(res * 43560)

                break
            count += 1
            if count + 1 == len(df["facts"][i]):
                lotsize.append(0)


df = clean(df)
df.to_csv(path_or_buf = "cleaned2.csv")