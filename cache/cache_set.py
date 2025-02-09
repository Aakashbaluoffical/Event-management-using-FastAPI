from configuration.connection import CACHEKEY
from cache import utility
import json
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from storage import query_data


CACHEKEY  = CACHEKEY()



def get_all_events(db):
    # try:
        # Retrieve data from cache asynchronously
    keys = CACHEKEY.ALL_EVENTS
    data = utility.get_data(key=keys)
    cache = False
    
    if data is not None:
        cache = True
        print("from cache")
    else:
        print("Without  cache")

        # Query data if not found in cache
        data =  query_data.get_all_events(db)
        
        if data is not None:
            cache = False
            
            state = utility.set_data(key=keys, value= data)
            
        
            if state is True:
                    print('Cache Set Successfully') 
        
        else:
            print('No data retrieved from query')
    
    return data

def get_all_registrated_events(db,user_id,owner):
    # try:
        # Retrieve data from cache asynchronously
    keys = CACHEKEY.ALL_REGISTRATED_EVENTS+str(user_id)+str(owner)
    data = utility.get_data(key=keys)
    cache = False
    
    if data is not None:
        cache = True
        print("from cache")
    else:
        print("Without  cache")

        # Query data if not found in cache
        data =  query_data.get_all_registrated_events(db,user_id,owner)
        
        if data is not None:
            cache = False
            
            state = utility.set_data(key=keys, value= data)
            
        
            if state is True:
                    print('Cache Set Successfully') 
        
        else:
            print('No data retrieved from query')
    
    return data



# def get_all_events(db):
#     # try:
#         # Retrieve data from cache asynchronously
#     keys = CACHEKEY.ALL_EVENTS
#     data = utility.get_data(key=keys)
#     cache = False
    
#     if data is not None:
#         cache = True
#         print("from cache")
#     else:
#         print("Without  cache")

#         # Query data if not found in cache
#         data =  query_data.get_all_events(db)
        
#         if data is not None:
#             cache = False
#             data = json.dumps(jsonable_encoder(data))
#             print("datadatadatadatadata",data)
#             state = utility.set_data(key=keys, value= data)
            
        
#             if state is True:
#                     print('Cache Set Successfully') 
        
#         else:
#             print('No data retrieved from query')

#         # Load data from JSON
#     print("loadsloads",data)
#     if data:
#         data = json.loads(data)  
    
#     return data