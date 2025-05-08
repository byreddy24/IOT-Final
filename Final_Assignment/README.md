# IoT Sensor Data Analysis - Final Assignment

This project collects, stores, and analyzes environmental and sound sensor data using an end-to-end pipeline powered by MQTT, Telegraf, InfluxDB, and Python. It is developed as part of the IOT final assignment.

---

## Project Structure

```
Final_Assignment/
├── data/
│ ├── influx_data.csv
│ ├── cleaned_data.csv
├── src/
│ ├── influx_utils.py
│ ├── cleandata.py
│ ├── plotting.py
├── README.md
├── pyproject.toml
├── poetry.lock
└── noshare.toml
```
---

## Pipeline Overview

1. **Sensors** (e.g., DHT22, MAX4466) are connected to a **Raspberry Pi**
2. Data is published using the **MQTT** protocol
3. **Telegraf** subscribes to MQTT topics and pushes data into **InfluxDB**
4. Python scripts fetch and process the data for visualization and analysis

---

## Sensors Used
- `DHT22`
- `MAX4466`
- `TSL2561`

---

## Data Tracked

- `temperature` (°C)
- `humidity` (%)
- `light_lux` (lux)
- `sound_rms` (Root Mean Square of sound)

---