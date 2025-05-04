import pandas as pd
from sklearn.preprocessing import PowerTransformer

class DataPreprocessor:
    def __init__(self):
        self.norm = PowerTransformer()

    def clean_data(self, df):
        drop_columns = [
            'total transactions (including tnx to create contract', 'total ether sent contracts',
            'max val sent to contract', ' ERC20 avg val rec', ' ERC20 max val rec',
            ' ERC20 min val rec', ' ERC20 uniq rec contract addr', 'max val sent',
            ' ERC20 avg val sent', ' ERC20 min val sent', ' ERC20 max val sent',
            ' Total ERC20 tnxs', 'avg value sent to contract', 'Unique Sent To Addresses',
            'Unique Received From Addresses', 'total ether received', ' ERC20 uniq sent token name',
            'min value received', 'min val sent', ' ERC20 uniq rec addr'
        ]
        drops1 = ['min value sent to contract', ' ERC20 uniq sent addr.1']
        drops2 = [
            ' ERC20 avg time between sent tnx', ' ERC20 avg time between rec tnx',
            ' ERC20 avg time between rec 2 tnx', ' ERC20 avg time between contract tnx',
            ' ERC20 min val sent contract', ' ERC20 max val sent contract',
            ' ERC20 avg val sent contract', ' ERC20 most sent token type',
            ' ERC20_most_rec_token_type'
        ]

        df.drop(columns=[col for col in drop_columns if col in df.columns], inplace=True, errors='ignore')
        df.drop(drops1 + drops2, axis=1, inplace=True, errors='ignore')

        for col in [' ERC20 uniq rec token name', ' ERC20 uniq sent addr',
                    ' ERC20 total ether sent', ' ERC20 total Ether received',
                    ' ERC20 total Ether sent contract']:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        return df

    def transform(self, df):
        transformed = self.norm.fit_transform(df)
        return pd.DataFrame(transformed, columns=df.columns)
