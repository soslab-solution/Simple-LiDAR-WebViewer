import argparse

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse

import json
import base64

from frame_handler import FrameHandler

fh = FrameHandler(dataset_dir="./samples")

app = FastAPI()

# serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
        <html>
            <head>
                <title>SOSLAB LiDAR Web app</title>
            </head>
            <body>
                <h1> ... </h1>
            </body>
        </html>
    """

@app.post('/api/loadDataset')
async def loadDataset(request: Request):
    data = {}
    data['dataset_path'] = fh.get_dataset_path()
    data['dataset_name'] = fh.get_dataset_name()
    data['dataset_len']  = fh.get_dataset_len() 
    response = JSONResponse(content=data)
    return response

@app.post('/api/loadPointCloud')
async def loadPointCloud(request: Request):
    frame_num = await request.json() 
    points_ = fh.get_lidar(frame_num)
    points = points_[:,:3]      # only send x,y,z points
    points_str = base64.b64encode(points.tobytes()).decode("utf-8")
    return points_str

@app.post('/api/loadImage')
async def loadImage(request: Request):
    frame_num = await request.json()
    img = fh.get_img(frame_num)
    return img

@app.post('/api/loadAnnotation')
async def loadAnnotation(request: Request):
    frame_num = await request.json()
    annos = fh.get_annos(frame_num)
    response = json.dumps(annos)
    return response
