import warnings
from datetime import datetime

import pandas as pd
# from flask import Flask, jsonify
# import matplotlib.pyplot as plt
import requests
from pandas_datareader import data as web

warnings.simplefilter('ignore')

url = 'http://www.fundamentus.com.br/resultado.php'

def analysis_fund():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }

    r = requests.get(url, headers=header)
    df = pd.read_html(r.text, decimal=',', thousands='.')[0]
    for coluna in ['Div.Yield', 'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Cresc. Rec.5a']:
        df[coluna] = df[coluna].str.replace('.', '')
        df[coluna] = df[coluna].str.replace(',', '.')
        df[coluna] = df[coluna].str.rstrip('%').astype('float') / 100
    df = df[df['Liq.2meses'] > 1000000]
    ranking = pd.DataFrame()
    ranking['pos'] = range(1, 151)
    ranking['EV/EBIT'] = df[df['EV/EBIT'] > 0].sort_values(by=['EV/EBIT'])['Papel'][:150].values
    ranking['ROIC'] = df.sort_values(by=['ROIC'], ascending=False)['Papel'][:150].values
    a = ranking.pivot_table(columns='EV/EBIT', values='pos')
    b = ranking.pivot_table(columns='ROIC', values='pos')
    t = pd.concat([a, b])
    rank = t.dropna(axis=1).sum()
    print(rank.sort_values()[:15])