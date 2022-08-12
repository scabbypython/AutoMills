import yfinance as yf
from sklearn.model_selection import GridSearchCV
import numpy as np
import xgboost as xgb
from sklearn.model_selection import KFold
import neptune.new as neptune
from sklearn.metrics import mean_squared_error
import tensorflow as tf

sp500_data = yf.download('^GSPC', start="1980-01-01", end="2021-11-21")
sp500_data = sp500_data[['Close']]
difs = (sp500_data.shift() - sp500_data) / sp500_data
difs = difs.dropna()
y = difs.Close.values
# create windows
X_data = []
y_data = []
for i in range(len(y) - 3*31):
    X_data.append(y[i:i+3*31])
    y_data.append(y[i+3*31])
X_windows = np.vstack(X_data)
# create train test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_windows, np.array(y_data), test_size=0.2, random_state=1)
X_train, X_val, y_train, y_val  = train_test_split(X_train, y_train, test_size=0.25, random_state=1)
# build LSTM using tensorflow keras

archi_list = [
              [tf.keras.layers.LSTM(32, return_sequences=True,  input_shape=(3*31,1)),
               tf.keras.layers.LSTM(32, return_sequences=True),
               tf.keras.layers.Dense(units=1)
               ],
              [tf.keras.layers.LSTM(64, return_sequences=True,  input_shape=(3*31,1)),
               tf.keras.layers.LSTM(64, return_sequences=True),
               tf.keras.layers.Dense(units=1)
               ],
              [tf.keras.layers.LSTM(128, return_sequences=True,  input_shape=(3*31,1)),
               tf.keras.layers.LSTM(128, return_sequences=True),
               tf.keras.layers.Dense(units=1)
               ],
              [tf.keras.layers.LSTM(32, return_sequences=True,  input_shape=(3*31,1)),
               tf.keras.layers.LSTM(32, return_sequences=True),
               tf.keras.layers.LSTM(32, return_sequences=True),
               tf.keras.layers.Dense(units=1)
               ],
              [tf.keras.layers.LSTM(64, return_sequences=True,  input_shape=(3*31,1)),
               tf.keras.layers.LSTM(64, return_sequences=True),
               tf.keras.layers.LSTM(64, return_sequences=True),
               tf.keras.layers.Dense(units=1)
               ],
 
]
 
for archi in archi_list:
    run = neptune.init(
          project="pythonscab/automills",
          api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJjY2ZmZjM3YS00ZjE0LTRjZWQtYjk5Ny01MzU0ZWNmNGI0YzgifQ==",
      )
    
    run['params'] = str(len(archi) - 1) + ' times ' + str(archi[0].units)
    run['Tags'] = 'lstm'
 
    
    lstm_model = tf.keras.models.Sequential(archi)
    lstm_model.compile(loss=tf.losses.MeanSquaredError(),
                      optimizer=tf.optimizers.Adam(),
                      metrics=[tf.metrics.MeanSquaredError()]
                      )
    history = lstm_model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))
    run['last_mse'] = history.history['val_mean_squared_error'][-1]    
    run.stop()