
"""
Settings for the complete test suite
"""
# Connection information
broker = "127.0.0.1"
port = 1883
qos = 0
user = None
password = None

sleep_interval = 2
topic = "ATM/location/measurements/"

location_id5 = 1105
location_id4 = 1104
location_id3 = 1103
location_id2 = 1102
location_id1 = 1101

# location IDs mapping to location names
locations = {
    1101 : "Marathahalli",
    1102 : "HSR Layout",
    1103 : "K R Puram",
    1104 : "C V Raman Nagar",
    1105: "Kadubeesanahalli",
    1106: "Silk board"
}