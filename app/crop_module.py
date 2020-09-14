import pandas

df = pandas.read_csv('data/usda_crops_5yr.csv')
df.fillna(0, inplace=True)

class crop_module:
    # Init
    def __init__(self):
        print('init crop_module')

    # get_county
    # id: takes FIPS_CODE
    def get_county(self, fips):
         selection = df.loc[df['FIPS_CODE'] == float(fips)]
         return selection.to_json(orient='records')

    # get_county
    # id: takes STATE_CODE
    def get_state(self, code, formatted=False):
         selection = df.loc[df['STATE_CODE'] == code.upper()]

         if formatted:
             summaryObject = {}
             counties = selection['COUNTY_NAME'].unique()

             for county in counties:
                 summaryObject[str(county)] = {}
                 countySubset = selection.loc[selection['COUNTY_NAME'] == county]
                 countySubsetCrops = countySubset['CROP'].unique()

                 for crop in countySubsetCrops:
                     cropData = countySubset.loc[countySubset['CROP'] == crop]
                     summaryObject[str(county)][crop] = cropData.to_dict('records')

             return summaryObject
         else:
             return selection.to_json(orient='records')

    # get_crop
    # id: takes CROP
    def get_crop(self, name, formatted=False):
         selection = df.loc[df['CROP'] == name.upper()]

         if formatted:
             summaryObject = {}
             states = selection['STATE_CODE'].unique()

             summaryObject['allStates'] = {
                'minYield': selection['TOTAL_YIELD'].min(),
                'averageYield': selection['TOTAL_YIELD'].mean(),
                'maxYield': selection['TOTAL_YIELD'].max(),
                'minAcres': selection['TOTAL_HARVESTED_ACRES'].min(),
                'averageAcres': selection['TOTAL_HARVESTED_ACRES'].mean(),
                'maxAcres': selection['TOTAL_HARVESTED_ACRES'].max()
             }

             for state in states:
                 # Compile summary stats by state, since our top level vis is at state level
                 subset = selection.loc[selection['STATE_CODE'] == state]
                 years = subset['YEAR'].unique()
                 summaryObject[state] = {}

                 # Compile overview for all year
                 summaryObject[state]['allTime'] = {
                    'minYield': subset['TOTAL_YIELD'].min(),
                    'averageYield': subset['TOTAL_YIELD'].mean(),
                    'maxYield': subset['TOTAL_YIELD'].max(),
                    'minAcres': subset['TOTAL_HARVESTED_ACRES'].min(),
                    'averageAcres': subset['TOTAL_HARVESTED_ACRES'].mean(),
                    'maxAcres': subset['TOTAL_HARVESTED_ACRES'].max()
                 }

                 for year in years:
                     # Compile yearly overviews
                     yearStats = subset.loc[selection['YEAR'] == year]

                     summaryObject[state][str(year)] = {
                        'minYield': yearStats['TOTAL_YIELD'].min(),
                        'averageYield': yearStats['TOTAL_YIELD'].mean(),
                        'maxYield': yearStats['TOTAL_YIELD'].max(),
                        'minAcres': yearStats['TOTAL_HARVESTED_ACRES'].min(),
                        'averageAcres': yearStats['TOTAL_HARVESTED_ACRES'].mean(),
                        'maxAcres': yearStats['TOTAL_HARVESTED_ACRES'].max()
                     }

             return summaryObject
         else:
             return selection.to_json(orient='records')
