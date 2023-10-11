# Group - Watchmen

# This is the face recognition server side code.
# This script connects to the mqtt broker, gets the IP of the camera web server and then gets images from the web server.

#Importing required libraries
import paho.mqtt.client as mqtt #for mqtt topic subscription
import requests #for downloading image from the camera web server
from playsound import playsound #for playing the pre-recorded sound
import face_recognition #for facial recognition

#encoding the images and saving the facial data for every image
picture_of_me = face_recognition.load_image_file("faces/kartik1.jpg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
picture_of_ripu = face_recognition.load_image_file("faces/ripu1.jpg")
ripu_face_encoding = face_recognition.face_encodings(picture_of_ripu)[0]
picture_of_manan = face_recognition.load_image_file("faces/manan.jpg")
manan_face_encoding = face_recognition.face_encodings(picture_of_manan)[0]
picture_of_vansh = face_recognition.load_image_file("faces/vansh1.jpg")
vansh_face_encoding = face_recognition.face_encodings(picture_of_vansh)[0]
picture_of_sir = face_recognition.load_image_file("faces/nair_sir.jpeg")
sir_face_encoding = face_recognition.face_encodings(picture_of_sir)[0]

#making a list of the known faces
known_faces = [
    my_face_encoding,
    ripu_face_encoding,
    manan_face_encoding,
    vansh_face_encoding,
    sir_face_encoding
]

#start the connection for downloading the image
def start_connection(url):
    flag=0
    while(True):
        try:
            #if response is found, we save the image to image.jpg
            response1 = requests.get(url, timeout = 5)

            with open("image.jpg", "wb") as f:
                f.write(response1.content)
                
            try:
                #encoding the downloaded image
                unknown_picture = face_recognition.load_image_file("image.jpg")
                unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
                #comparing the downloaded image with the known faces
                results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
                #if there is a match, play the respective sound
                if results[0] and flag!=1 :
                    playsound('kartikey.mp3')
                    flag=1
                elif results[1] and flag!=2 :
                    playsound('ripu.mp3')
                    flag=2
                elif results[2] and flag!=3 :
                    playsound('manan.mp3')
                    flag=3
                elif results[3] and flag!=4 :
                    playsound('vansh.mp3')
                    flag=4
                elif results[4] and flag!=5 :
                    playsound('nair_sir.mp3')
                    flag=5
            except:
                print("no face")
                flag=0
        except:
            print(1)
            break
        
#mqtt message receiving interrupt service routine
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")#printing the message
    url = str(message.payload.decode())#getting the ip
    url1 = "http://"+url+"/capture"
    print(url1)
    start_connection(url1)#starting the connection onto that ip

#stating the broker address and topic
broker_address = "91.121.93.94"
topic = "ssl/localip"

#subscribing to the mqtt broker
client = mqtt.Client()
client.connect(broker_address)
client.subscribe(topic)
client.on_message = on_message
print('mqtt server connected')

#client on loop untill it receives a message
client.loop_forever()
