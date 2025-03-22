df_cv = cross_validation(prophet_model, initial=initial, period=period, horizon=horizon)

df_p = performance_metrics(df_cv)

print(df_p.head())