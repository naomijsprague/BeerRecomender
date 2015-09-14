import pandas as pd 
import numpy as np
from pymongo import MongoClient
client = MongoClient()
db = client.untappd
db.collection_names()

