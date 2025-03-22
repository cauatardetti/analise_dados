import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from prophet.diagnostics import cross_validation, performance_metrics 

df = pd.read_csv('relatorio_clinicweb.csv', parse_dates=['Dia'], encoding="ISO-8859-1")

df = df[['Dia', 'Valor usado (BRL)']]


df = df.dropna()

df = df.set_index('Dia').resample('ME').sum()   

train = df.loc[:'2023-12']
test = df.loc['2024-01':'2024-12']


df_prophet = df.reset_index().rename(columns={'Dia':'ds', 'Valor usado (BRL)': 'y'})

initial = '365 days'  
period = '90 days'    
horizon = '365 days'

prophet_model = Prophet(changepoint_prior_scale=0.5, seasonality_prior_scale=10.0, holidays_prior_scale=10.0, seasonality_mode='additive', changepoint_range=0.9)



prophet_model.fit(df_prophet)
df_cv = cross_validation(prophet_model, initial=initial, period=period, horizon=horizon)

df_p = performance_metrics(df_cv)

print(df_p.head())
future = prophet_model.make_future_dataframe(periods=12, freq='ME')




forecast_prophet = prophet_model.predict(future)
forecast_prophet_test = forecast_prophet.loc[forecast_prophet['ds'].isin(test.index)]

prophet_rmse = np.sqrt(mean_squared_error(test['Valor usado (BRL)'], forecast_prophet_test['yhat']))
prophet_mae = mean_absolute_error(test['Valor usado (BRL)'], forecast_prophet_test['yhat'])

print('Prophet RMSE:', prophet_rmse)
print('Prophet MAE:', prophet_mae)

print('Prophet Forecast:')
print(forecast_prophet[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])