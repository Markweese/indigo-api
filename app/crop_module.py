import pandas

df = pandas.read_csv('../data/usda_crops_5yr.csv')

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
    # id: takes FIPS_CODE
    def get_state(self, code):
         selection = df.loc[df['STATE_CODE'] == code.upper()]
         return selection.to_json(orient='records')
