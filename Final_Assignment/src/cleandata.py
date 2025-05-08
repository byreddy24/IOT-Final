import pandas as pd
import pytz

# Load data
df = pd.read_csv("D:\RowanSemIV\_IOT\Final_Assignment\data\influx_data.csv")

# Convert '_time' to datetime
df["_time"] = pd.to_datetime(df["_time"], utc=True)

df["_time"] = df["_time"].dt.tz_convert("US/Eastern")

# Drop unnnecessary columns
df_clean = df.drop(columns=["result", "table", "_start", "_stop", "_measurement", "host", "topic"])
df_clean = df_clean.pivot(index="_time", columns="_field", values="_value").reset_index()
# Save cleaned data
df_clean.to_csv("D:\RowanSemIV\_IOT\Final_Assignment\data\cleaned_data.csv", index=False)
print("Cleaned data saved")
print(df.info())
print(df.head())