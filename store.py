# -*- coding: utf-8 -*-
import pymongo as pymongo

HOST = '127.0.0.1'
PORT = 27017
client = pymongo.MongoClient(HOST, PORT)
NewsDB = client.NewsDB