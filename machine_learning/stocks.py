import yfinance as yf
import numpy as np
import xgboost as xgb
from sklearn.model_selection import KFold
import neptune.new as neptune
from sklearn.metrics import mean_squared_error
sp500_data = yf.download('^GSPC', start="1980-01-01", end="2021-11-21")
sp500_data = sp500_data[['Close']]
 
 
difs = (sp500_data.shift() - sp500_data) / sp500_data
difs = difs.dropna()
 
y = difs.Close.values

# window through the data
X_data = []
y_data = []
for i in range(len(y) - 31):
    X_data.append(y[i:i+30])
    y_data.append(y[i+30])

X_windows = np.vstack(X_data)


 
# specify the grid for the grid search of hyperparameter tuning
parameters={'max_depth': list(range(2, 20, 4)),
            'gamma': list(range(0, 10, 2)),
            'min_child_weight' : list(range(0, 10, 2)),
            'eta': [0.01,0.05, 0.1, 0.15,0.2,0.3,0.5]
    }

param_list = [(x, y, z, a) for x in parameters['max_depth'] for y in parameters['gamma'] for z in parameters['min_child_weight'] for a in parameters['eta']]
 
 
for params in param_list:
 
    mses = []
 
    run = neptune.init(
          project="pythonscab/automills",
          api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJjY2ZmZjM3YS00ZjE0LTRjZWQtYjk5Ny01MzU0ZWNmNGI0YzgifQ==",
      )
    
    run['params'] = params
 
    my_kfold = KFold(n_splits=10, shuffle=True, random_state=0)
 
    for train_index, test_index in my_kfold.split(X_windows):
 
 
        X_train, X_test = X_windows[train_index], X_windows[test_index]
        y_train, y_test = np.array(y_data)[train_index], np.array(y_data)[test_index]
 
        xgb_model = xgb.XGBRegressor(max_depth=params[0],gamma=params[1], min_child_weight=params[2], eta=params[3])
        xgb_model.fit(X_train, y_train)
        preds = xgb_model.predict(X_test)
 
        mses.append(mean_squared_error(y_test, preds))
 
    average_mse = np.mean(mses)
    std_mse = np.std(mses)
    run['average_mse'] = average_mse
    run['std_mse'] = std_mse
    
        
    run.stop()