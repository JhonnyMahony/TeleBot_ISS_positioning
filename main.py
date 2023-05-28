import telebot
import json
import turtle
import urllib.request
import requests
import time
from PIL import Image
from math import radians, cos, sin, asin, sqrt
from telebot import types
import tkinter as TK
# API initialization
bot = telebot.TeleBot("6058109923:AAHo8RJs109hAG-aIqelpJbcodWVlb27AkE")

# The function of converting eps format into png format
def convert_eps_to_png(file_to_convert):
    TARGET_BOUNDS = (1024, 1024)

    pic = Image.open(file_to_convert)
    pic.load(scale=10)

    if pic.mode in ('P', '1'):
        pic = pic.convert("RGB")

    ratio = min(TARGET_BOUNDS[0] / pic.size[0],
                TARGET_BOUNDS[1] / pic.size[1])
    new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))

    pic = pic.resize(new_size, Image.ANTIALIAS)

    pic.save("image.png")

# Distance calculation function
def haversine(lon1, lat1, lon2, lat2):

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # формула гаверсинуса
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # The radius of the Earth in kilometers is 6371
    km = 6371 * c
    
    return km
    
@bot.message_handler(commands=["start"])

def start(message):
    mess = f"<b>Привіт {message.from_user.first_name}</b> введіть місто"
    bot.send_message(message.chat.id,mess, parse_mode="html")
    
@bot.message_handler(content_types=["text"])

def get_user_txt(message):
    try:
        # Obtaining the coordinates of the entered city
        key = "RKUObYVj7aJH3AgAufxTrjs0egP4brsB"
        url = "https://www.mapquestapi.com/geocoding/v1/address?key="
        loc = message.text
        main_url = url + key + "&location=" + loc
        r = requests.get(main_url)
        data = r.json()["results"][0]
        location = data["locations"][0]
        lat1 = location["latLng"]["lat"]
        lon1 = location["latLng"]["lng"]

        # Obtaining the coordinates of the ISS
        url = "http://api.open-notify.org/iss-now.json"
        response = urllib.request.urlopen(url)
        result = json.loads(response.read())

        location = result['iss_position']
        lat = float(location["latitude"])
        lon = float(location["longitude"])

        # Displaying the map on the screen
        screen = turtle.Screen()
        screen.setup(720, 360)
        screen.setworldcoordinates(-180, -90, 180, 90)
        screen.bgpic("map.gif")

        # Putting the ISS on the map

        screen.register_shape("iss.gif")
        iss = turtle.Turtle()
        iss.shape("iss.gif")
        iss.setheading(90)

        iss.penup()
        iss.goto(lon, lat)

        # Putting a dot on the coordinates of the city

        location = turtle.Turtle()
        location.penup()
        location.color("yellow")
        location.goto(lon1+4, lat1)
        location.dot(5)
        location.hideturtle()

        # Saving the image in eps format

        ts = turtle.getscreen()
        ts.getcanvas().postscript(file="duck.eps")

        # other
        location.clear()

        convert_eps_to_png("duck.eps")

        photo = open("image.png", "rb")

        bot.send_photo(message.chat.id, photo)
        photo.close()
        bot.send_message(message.chat.id, f"До міста {loc} від МКС {int(haversine(lon1, lat1, lon, lat))} кілометрів", parse_mode="html")
        try:
            TK.mainloop()
        except:
            print("l")
    except:
        bot.send_message(message.chat.id, "Щось пішло не так", parse_mode="html")



bot.polling()
