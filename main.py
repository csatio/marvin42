import requests
from datetime import datetime
import pandas as pd
import time
import json
import os
urlbase = 'https://mighty-bastion-45199.herokuapp.com/'

def get_result(x):
    try:
        result = pd.DataFrame.from_dict(x.json())
    except:
        result = x.text
    return result

def api_post(route, payload):
    url = urlbase + route
    x = requests.post(url, data = payload)
    df = get_result(x)
    return df

def api_get(route):
    url = urlbase + route
    x = requests.get(url)
    df = get_result(x)
    return df


def meu_modelo_linear_dummy(df):
  if random.randint(0,1) == 1:
    return 30
  else:
    return -30

def tratamento_df(df):
  return df.tail(1)
 
while True:
  df = api_post('cripto_quotation', {'token': token, 'ticker': 'BTCUSDT'})
  df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
  ## operacoes de feature eng. conforme o treinamento
  df_tratado = tratamento_df(df)
  tendencia = meu_modelo_linear_dummy(df_tratado)

  if tendencia > 0:
    payload = {'token': token,
              'ticker': 'BTCUSDT',
                'quantity': 1}

    api_post('buy', payload)
    print('buy')
  else:
      payload = {'token': token,
              'ticker': 'BTCUSDT',
                'quantity': 1}
      # ver se eu tenho bitcoin e, se tiver, vende
      api_post('sell', payload)
      print('sell')
  payload = {'token': token}
  print(api_post('status', payload))
  time.sleep(60)