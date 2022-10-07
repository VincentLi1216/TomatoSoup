import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
import time

first_time_running_code = "yes"

cred = credentials.Certificate("tomatosoup-id-firebase-adminsdk-yb0q8-6fc523611c.json")
firebase_admin.initialize_app(cred)
# app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    global first_time_running_code
    global take_photo_request
    take_photo_request_doc = db.collection(u'requests').document(u'take_photo_request').get()
    if first_time_running_code == "yes":
        print("Listener activated.")
        first_time_running_code = "no"
        return 0
    for doc in doc_snapshot:
        print(f'Received document snapshot: "{doc.id}" was modified')
    if take_photo_request_doc.to_dict()["request_todo"] == True and take_photo_request_doc.to_dict()["request_completed"] == False:
        update_photo_path("/home/ubuntu/static/wallpaper.jpg123")
        request_todo_false()
        request_completed_true()
    callback_done.set()

def update_photo_path(path):
    take_photo_request.update({u'photo_path': f'{path}'})

def request_todo_false():
    take_photo_request.update({u'request_todo': False})

def request_completed_true():
    take_photo_request.update({u'request_completed': True})

# 設定listener監聽的doc
take_photo_request = db.collection(u'requests').document(u'take_photo_request')
doc_ref = db.collection(u'requests').document(u'take_photo_request')

# 初始化
update_photo_path("/home/ubuntu/static/wallpaper.jpg")
take_photo_request.update({u'request_todo': False})
take_photo_request.update({u'request_completed': True})

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

# Nonstop code
while 1:
    time.sleep(1000)