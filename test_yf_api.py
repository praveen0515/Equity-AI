import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
res = requests.get('https://query2.finance.yahoo.com/v8/finance/chart/TCS.NS?range=6mo&interval=1d', headers=headers)
data = res.json()
meta = data['chart']['result'][0]['meta']
print("Price:", meta.get('regularMarketPrice'))
