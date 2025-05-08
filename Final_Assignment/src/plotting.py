import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Load data
df_cleaned = pd.read_csv("D:\RowanSemIV\_IOT\Final_Assignment\data\cleaned_data.csv")
df_cleaned["_time"] = pd.to_datetime(df_cleaned["_time"]).dt.tz_localize(None)

# Plot 1: Light Intensity Over Time
plt.figure(figsize=(14, 4))
light_threshold = df_cleaned["light_lux"].mean() - df_cleaned["light_lux"].std()
plt.plot(df_cleaned["_time"], df_cleaned["light_lux"], color="gray", label="Light Lux")
# Format x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%d %H:%M:%S'))
plt.title("Light Intensity Over Time (Sudden Drop Detection)")
plt.xlabel("Time")
plt.ylabel("Light Lux")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 2: Sound RMS with Threshold Background
plt.figure(figsize=(14, 5))
plt.axhspan(df_cleaned["sound_rms"].min(), 400, color='red', alpha=0.2, label="Below Threshold")
plt.axhspan(400, 600, color='blue', alpha=0.1, label="Normal Range")
plt.axhspan(600, df_cleaned["sound_rms"].max(), color='red', alpha=0.2, label="Above Threshold")
plt.plot(df_cleaned["_time"], df_cleaned["sound_rms"], color="black", linewidth=0.75, label="Sound RMS")
# Format x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%d %H:%M:%S'))
plt.axhline(y=400, color='gray', linestyle='--')
plt.axhline(y=600, color='gray', linestyle='--')
plt.title("Sound RMS with Threshold-Based Background Highlighting")
plt.xlabel("Time")
plt.ylabel("Sound RMS")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 3: Correlation Heatmap 
plt.figure(figsize=(10, 6))
sns.heatmap(df_cleaned.drop(columns=["_time", "sound_avg", "sound_db", "sound_voltage", "sound_raw", "sound_peak_to_peak"]).corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Between Sensor Readings")
plt.tight_layout()
plt.show()
