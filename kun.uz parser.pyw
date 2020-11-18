# author: Adxamjon97
# mail: adxamjon97@umail.uz 

import os
import json
import webbrowser

from tkinter  import Tk, Label, Button, Message, Frame, LEFT, RIGHT, TOP, BOTTOM, E, W
from PIL      import Image, ImageTk

from requests import get
from bs4      import BeautifulSoup as bs

URL = "https://kun.uz"

res = get(URL)

soup = bs(res.text, "lxml")
a = soup.find("a", class_="big-news")

# rasimni faylga saqledi
img = a.find(class_="big-news__img").img.get("src")
imgPath = "img\\"+ img.split("/")[-1]
res = get(img)

# img papka yaratadi agarda papka bo'lmasa
if not "img" in os.listdir():
    os.mkdir("img")

if os.path.exists(imgPath):
    print("Mavjud")
else:
    res = get(img)
    if res.status_code == 200:
        with open(imgPath, 'wb') as file:
            file.write(res.content)

# list qilib xotiraga olvolamiz
lst = {
    "url":   URL + a.get("href"),
    "img":   imgPath,
    "title": a.find(class_="big-news__title").text,
    "text":  a.find(class_="big-news__description").text,
    "data":  a.find(class_="news-meta").span.text
    }

# faylga saqlab boradi json farmatta
filename = "news.json"
data = []
if not os.path.exists(filename):
    with open(filename, "x") as new_file:
        json.dump([lst], new_file, indent=4)
else:
    with open(filename, "r") as read_file:
        data = json.load(read_file)

        if not lst in data:
            data.insert(0, lst)

        with open(filename, "w") as write_file:
            json.dump(data, write_file, indent=4)


# osson tushunish uchun interfeys
root = Tk()

col_left   = Frame(root)
col_center = Frame(root, width=800)
col_right  = Frame(root)

width  = 765 # размер окна
height = 555

x = int(root.winfo_screenwidth() //2 - width /2) # середина экрана
y = int(root.winfo_screenheight()//2 - height/2)

root.title("Kun uz yangiliklar")
root.resizable(False, False) 
root.geometry(f"{width}x{height}+{x}+{y}")

# so'ratni ko'rsatadi
load   = Image.open(imgPath)
render = ImageTk.PhotoImage(load)

img = Label(col_center, image = render, width=700) 
img.image = render 
img.pack()

# yozuvni ko'rsatadi
title = Message(col_center, text=lst["title"], font=(None, 13,"bold"), width=700, justify="center")
text  = Message(col_center, text=lst["text"],  font=(None, 13),        width=700, justify="center")
day   = Message(col_center, text=lst["data"],  font=(None, 10),        width=700, justify="left"  )

title.pack()
text.pack()
day.pack(side=LEFT)
#title["text"] = "test"

left  = Button(col_left,  text="left" )
right = Button(col_right, text="right")

left.pack()
right.pack()

link1 = Label(col_center, text="To'liq ma'lumot uchun >>", font=(None, 13,"italic"), fg="blue", cursor="hand2")
link1.bind("<Button-1>", lambda e: webbrowser.open_new(lst["url"]))
link1.pack(side=RIGHT)

n1 = 0
def edit(n=n1):
	global n1
	global load
	global render
	
	n1 = n if n>=0 and n<len(data) else n1 
	
	lst = data[n1]

	load   = Image.open(lst["img"])
	render = ImageTk.PhotoImage(load)

	img.config(image=render)
	root.update_idletasks()
		
	title["text"] = lst["title"]
	text["text"]  = lst["text"]
	day["text"]   = lst["data"]

	link1.bind("<Button-1>", lambda e: webbrowser.open_new(lst["url"]))

left.bind("<Button-1>", lambda e: edit(n1-1))
right.bind("<Button-1>", lambda e: edit(n1+1))

col_left.pack(side=LEFT)
col_center.pack(side=LEFT)
col_right.pack(side=LEFT)
root.mainloop()
