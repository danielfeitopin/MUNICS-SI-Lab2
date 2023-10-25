from paho.mqtt.client import Client
from config import MQTT_IP
from config import MQTT_KEEPALIVE
from config import MQTT_PASSWORD
from config import MQTT_PORT
from config import MQTT_USER_NAME

class MQTT(Client):

    MQTT_USER_NAME = MQTT_USER_NAME
    MQTT_PASSWORD = MQTT_PASSWORD
    MQTT_IP = MQTT_IP
    MQTT_PORT = MQTT_PORT
    MQTT_KEEPALIVE = MQTT_KEEPALIVE

    def __init__(self, id: str) -> None:
        super().__init__()
        self.ip: str = self.MQTT_IP
        self.id: str = id
        self.username_pw_set(username=self.MQTT_USER_NAME,
                             password=self.MQTT_PASSWORD)
        
        self.payload = None

    def on_connect(self, client, userdata, flags, rc):
        print(f'Connected with result code {rc}')
        client.subscribe(self.id)

    def connect(self):
        super().connect(self.MQTT_IP, self.MQTT_PORT, self.MQTT_KEEPALIVE)
        
    def on_message(self, client, userdata, message):
        print('Received message!', end=' ')
        print(f'Payload: {message.payload}')
        self.payload = message.payload
        self.disconnect()
