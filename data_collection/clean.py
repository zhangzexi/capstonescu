import pandas as pd
pd.options.mode.chained_assignment = None
df = pd.read_csv("dataset.txt")

def clean(dataFrame):
    dataFrame.drop("state", axis=1, inplace=True)
    dataFrame.drop("Unnamed: 0", axis=1, inplace=True)
    mask = (dataFrame.property_type != "Miscellaneous") & (dataFrame.property_type != "Multiple Occupancy") & (
    dataFrame.property_type != "Other") & (dataFrame.property_type.notnull()) & (dataFrame.property_type != "Mobile / Manufactured") & (
           dataFrame.property_type != "Multi Family")
    dataFrame = dataFrame[mask]
    dataFrame = pd.get_dummies(dataFrame, columns=["property_type"])
    dataFrame.index = [range(len(dataFrame))]
    return dataFrame

def getLot(df):
    lot_size = []
    for i in range(len(df.facts)):
        if "Lot:" in df.facts[i]:
            lot_index = df.facts[i].index("Lot:")
            lot_count = 0
            lot_length = 0
            for char in df.facts[i][lot_index:]:
                if char != "'":
                    lot_count += 1
                else:
                    lot_length = lot_count + lot_index
                    break

            lot = df.facts[i][lot_index:lot_length]
            if "sqft" in lot:
                if "," in lot:
                    lot_split = lot.split()[-2].split(",")
                    lot_value = ""
                    for n in lot_split:
                        lot_value += n
                else:
                    lot_value = lot.split()[-2]
                lot_size.append(int(lot_value))
            if "acre" in lot:
                lot_value = float(lot.split()[-2]) * 43560
                lot_size.append(int(lot_value))
        else:
            lot_size.append(0)
    return lot_size

def getBuilt(df):
    built_in = []
    for i in range(len(df.facts)):
        if "Built in" in df.facts[i]:
            built_index = df.facts[i].index("Built in")
            built_count = 0
            built_length = 0
            for char in df.facts[i][built_index:]:
                if char != "'":
                    built_count += 1
                else:
                    built_length = built_count + built_index
                    break

            built_value = df.facts[i][built_index:built_length].split()[-1]

            built_in.append(int(built_value))
        else:
            built_in.append(0)

    return built_in

def getView(df):
    all_time_views = []
    for i in range(len(df.facts)):
        if "All time views:" in df.facts[i]:
            view_index = df.facts[i].index("All time views:")
            view_count = 0
            view_length = 0
            for char in df.facts[i][view_index:]:
                if char != "'":
                    view_count += 1
                else:
                    view_length = view_count + view_index
                    break

            views = df.facts[i][view_index:view_length]
            if "," in views:
                views_split = views.split()[-1].split(",")
                views_value = ""
                for n in views_split:
                    views_value += n
            else:
                views_value = views.split()[-1]
            all_time_views.append(int(views_value))
        else:
            all_time_views.append(0)

    return all_time_views

def getSoldDate(df):
    sold_date = []
    for i in range(len(df.facts)):
        if "Last sold:" in df.facts[i]:
            sold_date_index = df.facts[i].index("Last sold:")
            sold_date_count = 0
            sold_date_length = 0
            for char in df.facts[i][sold_date_index:]:
                if char != "'":
                    sold_date_count += 1
                else:
                    sold_date_length = sold_date_count + sold_date_index
                    break

            date = df.facts[i][sold_date_index:sold_date_length].split()[2:4]
            res = date[0] + " " + date[1]
            sold_date.append(res)
        else:
            sold_date.append("N/A")

    return sold_date


df = clean(df)
# before running getLot function, change the following to avoid error due to errors in dataset
df.facts[94] = "['Lot: 6,800 sqft', 'Single Family', 'Built in 1922', 'All time views: 643', 'Last sold: Dec 2016 for $865,000', 'Last sale price/sqft: $630', 'Flooring: Hardwood', 'Parking: 252 sqft garage']"
df.facts[2647] = "['Lot: 46,609 sqft', 'Single Family', 'Built in 2005', 'All time views: 837', 'Last sold: Sep 2015 for $3,400,000', 'Last sale price/sqft: $850', 'Flooring: Hardwood, Tile']"
df.facts[2922] = "['Baths: 4 full, 1 half', 'Lot: 49,299 sqft', 'Single Family', 'Built in 1954', 'All time views: 13,381', 'Cooling: Central', 'Heating: Forced air, Radiant', 'Last sold: Jan 2017 for $4,740,000', 'Last sale price/sqft: $1,032', 'Ceiling Fan', 'Deck', 'Fenced Yard', 'Fireplace', 'Flooring: Hardwood, Tile, Other', 'Garden', 'Hot Tub/Spa', 'Lawn', 'Parking: Garage - Attached, 3 spaces, 836 sqft garage', 'Patio', 'Pool', 'Porch', 'Skylight', 'Vaulted Ceiling', 'View: Mountain']"
df.facts[6477] = "['Lot: 7,405 sqft', 'Single Family', 'Built in 1957', 'All time views: 4,322', 'Last sold: Feb 2015 for $3,100,000', 'Last sale price/sqft: $620', 'Great solar potential', u'Sun Number\\u2122:\\xa077', 'Flooring: Slate', 'Gated Entry', 'Parking: 504 sqft garage', 'Vaulted Ceiling']"
df.facts[7404] = "['Lot: 1,650 sqft', 'Single Family', 'Built in 1981', 'All time views: 4,877', 'HOA Fee: $41/mo', 'Last sold: Jun 2016 for $1,142,000', 'Last sale price/sqft: $816', 'Parking: 360 sqft garage']"
df.facts[8699] = "['Lot: 5,000 sqft', 'Single Family', 'Built in 1958', 'All time views: 358', 'Last sold: Jan 2017 for $640,000', 'Last sale price/sqft: $563', 'Limited solar potential', u'Sun Number\\u2122:\\xa046', 'Fireplace', 'Parking: 350 sqft garage']"
df.facts[8940] = "['Lot: 6,000 sqft', 'Single Family', 'Built in 1971', 'All time views: 641', 'Last sold: Jun 2016 for $101,500', 'Last sale price/sqft: $101,500', 'Great solar potential', u'Sun Number\\u2122:\\xa079', 'Fireplace', 'Parking: 399 sqft garage']"
df.facts[9049] = "['Lot: 5,356 sqft', 'Single Family', 'Built in 1958', 'All time views: 249', 'Last sold: Mar 2016 for $16,500', 'Last sale price/sqft: $18', 'Great solar potential', u'Sun Number\\u2122:\\xa083', 'Parking: 367 sqft garage']"
df.facts[9053] = "['Lot: 5,000 sqft', 'Single Family', 'Built in 1959', 'All time views: 729', 'Last sold: Mar 2016 for $113,500', 'Last sale price/sqft: $70', 'Candidate for a community solar program', u'Sun Number\\u2122:\\xa034', 'Fireplace', 'Parking: 350 sqft garage']"
df.facts[9093] = "['Lot: 5,200 sqft', 'Single Family', 'Built in 1959', 'All time views: 521', 'Last sold: Jan 2016 for $350,000', 'Last sale price/sqft: $312', 'Great solar potential', u'Sun Number\\u2122:\\xa083', 'Fireplace', 'Parking: 350 sqft garage']"
df.facts[9113] = "['Lot: 5,500 sqft', 'Single Family', 'Built in 1968', 'All time views: 411', 'Last sold: Dec 2015 for $350,000', 'Last sale price/sqft: $293', 'Candidate for a community solar program', u'Sun Number\\u2122:\\xa034', 'Parking: 446 sqft garage']"
df.facts[10286] = "['Lot: 6,534 sqft', 'Single Family', 'Built in 1978', 'All time views: 2,029', 'Last sold: Mar 2016 for $499,000', 'Last sale price/sqft: $405', 'Great solar potential', u'Sun Number\\u2122:\\xa073', 'Fireplace', 'Parking: 456 sqft garage']"
df.facts[10315] = "['Baths: 1 full, 1 half', 'Lot: 2,178 sqft', 'Townhouse', 'Built in 1982', 'All time views: 2,203', 'HOA Fee: $265/mo', 'Last sold: Feb 2016 for $395,500', 'Last sale price/sqft: $375', 'Limited solar potential', u'Sun Number\\u2122:\\xa052', 'Parking: 180 sqft garage']"
df.facts[10412] = "['Lot: 6,477 sqft', 'Single Family', 'Built in 1947', 'All time views: 255', 'Last sold: Oct 2015 for $241,500', 'Last sale price/sqft: $286', 'Great solar potential', u'Sun Number\\u2122:\\xa082', 'Parking: 264 sqft garage']"
df.facts[10446] = "['Lot: 6,222 sqft', 'Single Family', 'Built in 1942', 'All time views: 394', 'Last sold: Aug 2015 for $275,000', 'Last sale price/sqft: $221', 'Great solar potential', u'Sun Number\\u2122:\\xa076', 'Fireplace', 'Parking: Garage, 441 sqft garage']"

### run below to get new columns
df["lot_size_in_sqft"] = getLot(df)
df["year_built"] = getBuilt(df)
df["views"] = getView(df)
df["sold_date"] = getSoldDate(df)



print df
