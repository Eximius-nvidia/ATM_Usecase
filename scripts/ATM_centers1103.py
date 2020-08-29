import paho.mqtt.client as mqttClient
import time
import random
import json
import os


broker = "127.0.0.1"
port = 1883
location_id = 1103
sleep_interval = 2
qos = 0

topic = "ATM/location/measurements/"
payload = {
    "location" : "HSR Layout",
    "status" : 1,
    "temp_low" : 24,
    "temp_high" : 34,
}


def on_connect(client, userdata, flags, rc):
    """
    Method to perform initial connection operation
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    status = {0: "Connection successful",
              1: "Connection refused – incorrect protocol version",
              2: "Connection refused – invalid client identifier",
              3: "Connection refused – server unavailable",
              4: "Connection refused – bad username or password",
              5: "Connection refused – not authorised",
              6 - 255: "Currently unused"
              }
    print("-" * 60)
    text = "{:<27} : {}\n{:<27} : {}\n{:<27} : {}".format("Client connected to broker", client._host, "Client ID/Location ID", str(client._client_id,"UTF-8"), "Client status", status[rc])
    print(text)
    print("-" * 60)
    # Publish as the ATM is active
    client.publish("ATM/location/status/" + str(client._client_id, "UTF-8"), payload = json.dumps(payload), qos=1, retain= True)

def on_disconnect(client, userdata, rc):
    """
    On client disconnect
    :param client:
    :param userdata:
    :param rc:
    :return:
    """
    if client.is_connected() == False:
        print("Client disconnected............")
    else:
        print("Something gone wrong in Client disconnecting")

def control_ac(temp_low = 0, temp_high = 0, present_temp = 0):
    """
    Methos to Decides AC On/Off status
    :param temp_low:
    :param temp_high:
    :param present_temp:
    :return: On/Off Based on the validation rule
    """
    if  present_temp < temp_low:
        status = "Off"
    elif present_temp > temp_high:
        status = "On"
    # elif temp_low <= present_temp <= temp_high and status == "On":
        # status = "On"
    else:
        status = "Off"   
    return status


if __name__ == "__main__":

    os.system('cls')
    client = mqttClient.Client(str(location_id))  # create new instance
    # client.username_pw_set(user, password=password)  # set username and password
    client.on_connect = on_connect  # attach function to callback
    client.on_disconnect = on_disconnect
    # client.will_set("ATM/location/status/" + str(client._client_id, "UTF-8"), payload, qos=1, retain=True)
    client.connect(broker, port=port)  # connect to broker
    client.loop_start()  # start the loop

    while not client.is_connected():  # Wait for connection
        time.sleep(0.1)

    try:
        while True:

            payload1 = {}
            payload1['temp_present'] = random.randint(0,60) # Will be replaced with sensor's temperature
            payload1['ac_status'] = control_ac(payload["temp_low"], payload["temp_low"], payload1['temp_present'])
            topic_to_send = topic + str(location_id)
            # Publish the AC temperature and its status
            client.publish(topic_to_send, payload = json.dumps(payload1), qos=qos, retain= False)
            print("payload = {}".format(payload1))
            time.sleep(sleep_interval)

    except KeyboardInterrupt:
        # Publish as the ATM is inactive
        payload["status"] = 0
        client.publish("ATM/location/status/" + str(client._client_id, "UTF-8"), payload = json.dumps(payload), qos=1, retain=True)
        client.disconnect()
        client.loop_stop()
