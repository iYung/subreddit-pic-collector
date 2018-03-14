import numpy as np
import cv2
import os
import urllib
import requests as r
import sys

##variable assignments
subreddit = sys.argv[1]
path = './photos/' + subreddit
face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
last_post = ""

##functions
def getImg(url):
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    return image

def getFaces(url,id):
    image = getImg(url)
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if not face_cascade.empty():
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            i = 1
            for (x,y,w,h) in faces:
                crop_img = img[y:y+h, x:x+w]
                cv2.imwrite( os.path.join(path, id + "_" + str(i) + '.jpg') ,cv2.resize(crop_img, (50, 50)))
                i + 1
                
def getImgUrl(url,domain):
    if domain == "imgur.com":
        return "http://i.imgur.com/" + url.split("/")[-1] + ".jpg"
    return url

##main code
if not os.path.exists(path):
    os.makedirs(path)

for i in range(2):
    request = r.get("https://www.reddit.com/r/" + subreddit + "/top.json?after=" + last_post).json()
    if 'data' in request:
        for node in request['data']['children']:
            data = node['data'] 
            after = data['name']
            url = getImgUrl(data['url'],data['domain'])
            getFaces(url,data['id'])
            print data['id'] + " " + data['domain']