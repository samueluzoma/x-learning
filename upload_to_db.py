# import streamlit_authenticator as stauth

# import database as db

# usernames =["ellafari","nedu","fred","eniola"]
# names=["abubakar emmanuella", "anolue francis ", "sylva fred","eniola"]
# password =["fari123","nedu123","fred123","eniola123"]

# hash_passwords =stauth.Hasher(password).generate()

# for (username, name, hash_password) in zip(usernames,names,hash_passwords ):
#     db.insert_user(username,name,hash_password)

import streamlit_authenticator as stauth
# Make sure your database file is named database.py
import database as db 

# CHANGE THESE TO YOUR PREFERRED ACCOUNTS
usernames = ["aminat", "supervisor_1", "student_test"]
names = ["Ige Aminat Ayobami", "Project Supervisor", "Test Student"]
passwords = ["aminat2000", "supervisor123", "student123"]

# This creates the secure hashed versions
hash_passwords = stauth.Hasher(passwords).generate()

# This loop pushes them to the Deta Cloud
for (username, name, hash_password) in zip(usernames, names, hash_passwords):
    db.insert_user(username, name, hash_password)

print("Database initialized with new users!")