import toml
from influxdb_client import InfluxDBClient

# Load config from noshare.toml
def get_config(config_path):
    return toml.load(config_path)["influxdb"]

# Establish InfluxDB client
def get_influxdb_client(config_path):
    conf = get_config(config_path)
    return InfluxDBClient(
        url=conf["url"],
        token=conf["token"],
        org=conf["org"]
    )

# Query InfluxDB and return results as a Pandas DataFrame
def query_data_frame(config_path="noshare.toml"):
    conf = get_config(config_path)
    query = '''
    from(bucket: "OUTDOOR")
      |> range(start: 2025-05-07T23:00:00Z, stop: 2025-05-08T01:00:00Z)
      |> filter(fn: (r) => r["_measurement"] == "mqtt_consumer")
      |> filter(fn: (r) => r["topic"] == "OUTDOOREVENING/FINALE")
    '''

    client = get_influxdb_client(config_path)
    query_api = client.query_api()
    return query_api.query_data_frame(query)

if __name__ == "__main__":
    # Query the data
    df = query_data_frame()

    # Show basic info
    print("Data fetched from InfluxDB.")
    print(df.info())
    print(df.head())

    # Save to CSV
    df.to_csv("data/influx_data.csv", index=False)
    print("Data saved to influx_data.csv")