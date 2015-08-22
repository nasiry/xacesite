__author__ = 'jcteng'

import motor

uri = "mongodb://admin:admin@192.168.1.21:27017/database_name"
client = motor.MotorClient(uri)

db=client["admin"]