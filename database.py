# from deta import Deta
# import os
# from dotenv import load_dotenv
# import bcrypt



# load_dotenv(".env")
# DETA_KEY =os.getenv("DETA_KEY")


# deta=Deta(DETA_KEY) # to initialize the key and deta 

# #create a database connection 

# db= deta.Base("learnX_user_db")

# def insert_user(username, user_dict):
#     hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#     return db.put({"key":username, "name":user_dict["name"], "password":user_dict["password"]}) #the primary key is the username 


# # to fetch all the users 

# def db_fetch():
#     res =db.fetch()
#     return res.items
# print (db_fetch())


# # def update_user(username, updates):
# #     return db.update(updates,username)

# # update_user("ellafari", updates={"name":"laraba usman"})


# # def delete(username):
# #     return db.delete(username)
# # delete("ellafari")

from deta import Deta
import os
from dotenv import load_dotenv

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY2") # Ensure this matches your .env file

deta = Deta(DETA_KEY)

# CRITICAL: Ensure this name matches what you use in Home.py
db = deta.Base("learnX_main_db") 

def insert_user(username, name, hash_password):
    """
    Saves the user to the cloud.
    The 'key' is the username (must be unique).
    """
    return db.put({
        "key": username, 
        "name": name, 
        "password": hash_password
    })

def db_fetch():
    """Fetches all registered students for login validation"""
    res = db.fetch()
    return res.items

# To test if it's working, you can uncomment the line below:
# print(db_fetch())