from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from os import listdir
from os.path import join

from random import choice


with open('index.html', 'r') as html:
    html_raw = html.read()

IMAGES_PATH = join('.', 'images')
images_list = listdir(IMAGES_PATH)

with open('compliments.txt') as txt:
    compliments_list = txt.readlines()

def get_bytearray_of_image(path):
    with open(path, 'rb') as image:
        f = image.read()
        b = bytes(f)
        return b


origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def main_page():
    return HTMLResponse(html_raw)

@app.get('/image')
def get_image():
    random_image_path = join(IMAGES_PATH, choice(images_list))
    image_bytes = get_bytearray_of_image(random_image_path)
    return Response(content=image_bytes)

@app.get('/compliment')
def get_compliment():
    compliment = choice(compliments_list).strip()
    return {'compliment': compliment}



if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=80, reload=True)