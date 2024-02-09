from ast import literal_eval

import pandas as pd
from datasets import load_dataset


class DataPreprocessor:
    def __init__(self):
        self.data = load_dataset("JanosAudran/financial-reports-sec", "small_full", split="train")
        self.data = self.data.to_pandas()

    def parse_sentiment(self, label_dict):
        if isinstance(label_dict, str):
            label_dict = literal_eval(label_dict)
        return {
            '1_day_sentiment': 'positive' if label_dict['1d'] == 1 else 'negative',
            '5_day_sentiment': 'positive' if label_dict['5d'] == 1 else 'negative',
            '30_day_sentiment': 'positive' if label_dict['30d'] == 1 else 'negative',
        }

    def preprocess_data(self):
        self.data['filingDate'] = pd.to_datetime(self.data['filingDate'], errors='coerce')
        self.data = self.data[(self.data['cik'] == '0000001750') & (self.data['filingDate'].dt.year.isin([2019, 2020]))]
        expanded_sentiments = self.data['labels'].apply(self.parse_sentiment).apply(pd.Series)
        documents_df = pd.concat([self.data.drop(columns=['labels']), expanded_sentiments], axis=1)
        return documents_df.groupby('docID').agg({
            'sentence': ' '.join,
            'filingDate': 'first',
            'stateOfIncorporation': 'first',
            '1_day_sentiment': 'first',
            '5_day_sentiment': 'first',
            '30_day_sentiment': 'first'
        }).reset_index()
