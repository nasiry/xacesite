#!/usr/bin/python
# -*- coding:utf-8 -*-
#
__author__ = 'jcteng'


import motor

db_uri = "mongodb://192.168.1.21:27017"
db_name = "xacesite"
db_auth_collection="auth"
db_map_collection="map"
db_nav_collection="navi"

def filldb():
    motor.MotorDatabase.create_collection()


def motorInit():

    client = motor.MotorClient(db_uri)
    db= client[db_name]
    return db






dbinit()