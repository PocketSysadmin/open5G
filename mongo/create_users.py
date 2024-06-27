from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib


# Configuración de conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/') 
db = client['open5gs']  
collection = db['subscribers']

# Valores iniciales
initial_imsi = 208930000000001
initial_k = '0C0A34601D4F07677303652C0462535B'
initial_opc = '63bfa50ee6523365ff14c1f45f88737d'

# Función para generar nuevos valores k y opc
def increment_hex(hex_str, increment):
    return '{:032x}'.format(int(hex_str, 16) + increment)

# Número de usuarios a agregar
num_users = 10

for i in range(num_users):
    imsi = str(initial_imsi + i)
    k = increment_hex(initial_k, i)
    opc = increment_hex(initial_opc, i)
    
    subscriber = {
        "_id": ObjectId(),
        "imsi": imsi,
        "subscribed_rau_tau_timer": 12,
        "network_access_mode": 2,
        "subscriber_status": 0,
        "access_restriction_data": 32,
        "slice": [
            {
                "sst": 1,
                "default_indicator": True,
                "_id": ObjectId(),
                "session": [
                    {
                        "name": "internet",
                        "type": 3,
                        "_id": ObjectId(),
                        "pcc_rule": [],
                        "ambr": {
                            "uplink": {
                                "value": 1,
                                "unit": 3
                            },
                            "downlink": {
                                "value": 1,
                                "unit": 3
                            }
                        },
                        "qos": {
                            "index": 9,
                            "arp": {
                                "priority_level": 8,
                                "pre_emption_capability": 1,
                                "pre_emption_vulnerability": 1
                            }
                        }
                    }
                ]
            }
        ],
        "ambr": {
            "uplink": {
                "value": 1,
                "unit": 3
            },
            "downlink": {
                "value": 1,
                "unit": 3
            }
        },
        "security": {
            "k": k,
            "amf": "8000",
            "op": None,
            "opc": opc,
            "sqn": 97
        },
        "msisdn": [],
        "schema_version": 1,
        "__v": 0
    }
    
    collection.insert_one(subscriber)
    print(f"Usuario con IMSI {imsi} añadido.")

print("Proceso completado.")
