# WebViewer

<img src="viewer.gif">

## Requirements

- python >= 3.9
- fastapi
- open3d
- numpy

## RUN

1. Install requirements

   ```bash
   pip install fastapi open3d numpy uvicorn
   ```

2. Run app
   ```bash
   $ cd app
   $ uvicorn main:app --host 0.0.0.0 --port 7779 --reload
   ```
3. app 접속  
   `http://localhost:7779/static/index.html`
