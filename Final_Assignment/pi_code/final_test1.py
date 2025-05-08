import time
import json
import datetime
import statistics
import spidev
import Adafruit_DHT
import paho.mqtt.client as mqtt
import board
import busio
import toml
from adafruit_tsl2561 import TSL2561

# Sensor Configuration
SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin connected to DHT22
SOUND_CHANNEL = 0  # MCP3008 CH0

# MCP3008 SPI Setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1350000

def read_adc(channel):
    if not 0 <= channel <= 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) | adc[2]
    return data

# I2C Setup for TSL2561
i2c = busio.I2C(board.SCL, board.SDA)
tsl = TSL2561(i2c)
tsl.enable = True
tsl.gain = 0
tsl.integration_time = 1

# MQTT Configuration
config = toml.load("noshare.toml")["mqtt"]
MQTT_BROKER = config["broker"]
MQTT_PORT = config["port"]
MQTT_TOPIC = config["topic"]
MQTT_USER = config["username"]
MQTT_PASS = config["password"]

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

def get_sound_metrics(samples=100, delay=0.002):
    values = [read_adc(SOUND_CHANNEL) for _ in range(samples)]
    time.sleep(delay * samples)
    avg = statistics.mean(values)
    peak_to_peak = max(values) - min(values)
    rms = (sum(v**2 for v in values) / len(values)) ** 0.5
    return int(avg), int(peak_to_peak), round(rms, 2), values[-1]

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, DHT_PIN)
        temp_f = (temperature * 9/5) + 32 if temperature is not None else None

        avg_raw, p2p_raw, rms_raw, last_raw = get_sound_metrics()
        voltage = (avg_raw * 5.0) / 1023
        decibels = round(20 * (voltage / 5.0), 2) if voltage > 0 else 0

        lux = round(tsl.lux, 2) if tsl.lux is not None else None
        timestamp = datetime.datetime.now().isoformat()

        payload = {
            "temperature": round(temp_f, 1) if temp_f is not None else None,
            "humidity": round(humidity, 1) if humidity is not None else None,
            "sound_raw": last_raw,
            "sound_avg": avg_raw,
            "sound_peak_to_peak": p2p_raw,
            "sound_rms": rms_raw,
            "sound_voltage": round(voltage, 2),
            "sound_db": decibels,
            "light_lux": lux,
            "timestamp": timestamp
        }

        result = client.publish(MQTT_TOPIC, json.dumps(payload))
        if result.rc == 0:
            print(f"Published to {MQTT_TOPIC}: {json.dumps(payload)}")
        else:
            print("Failed to publish message")

        time.sleep(3)

except KeyboardInterrupt:
    print("Exiting...")
    spi.close()
    client.loop_stop()
    client.disconnect()
