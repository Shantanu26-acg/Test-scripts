import pandas as pd

dp=pd.read_excel("Master data.xlsx", sheet_name='URLs')

serialization_url=dp.iloc[2, 0]
login_url=dp.iloc[0, 0]

print(serialization_url)