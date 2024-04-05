# import boto3
# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# import requests

# app = FastAPI()
# s3 = boto3.client('s3')

# # Variable to store the last uploaded file name
# last_uploaded_file = None
# # Variable to store the firmware version
# firmware_version = "0.0.1"
# # Variable to track total files downloaded
# total_files_downloaded = 0

# # HTML form for file upload and firmware manipulation
# upload_form_html = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title> File Upload Form </title>
# </head>
# <body>
#     <h2>Current Firmware Version</h2>
#     <p>{firmware_version}</p>
#     <h2>Total Files Downloaded</h2>
#     <p>{total_files_downloaded}</p>

#     <h2>Upload firmware.bin file</h2>
#     <form action="/upload_file/" method="post" enctype="multipart/form-data">
#         <input type="file" name="file"><br><br>
#         <input type="submit" value="Upload">
#     </form>

#     <h2>Download last uploaded file</h2>
#     <form action="/get_file/" method="get">
#         <input type="submit" value="Download Last Uploaded File">
#     </form>
# </body>
# </html>
# """

# @app.get("/", response_class=HTMLResponse)
# async def home():
#     return upload_form_html.format(firmware_version=firmware_version, total_files_downloaded=total_files_downloaded)

# @app.get("/get_version/")
# async def get_version():
#     return {"version": firmware_version}

# @app.get("/set_version/")
# async def set_version(version: str):
#     global firmware_version
#     firmware_version = version
#     return {"message": "Firmware version set successfully", "version": firmware_version}

# @app.post("/upload_file/")
# async def upload_file(file: UploadFile = File(...)):
#     global last_uploaded_file
#     with open(file.filename, "wb") as buffer:
#         buffer.write(file.file.read())
#     last_uploaded_file = file.filename
#     return {"filename": file.filename}

# # @app.post("/upload_file/")
# # async def create_upload_file(file: UploadFile = File(...)):
# #     # Upload file to S3
# #     s3.upload_fileobj(file.file, 'your-bucket-name', file.filename)
# #     last_uploaded_file = file.filename
# #     return {"filename": file.filename}

# @app.get("/get_file/")
# async def get_file():
#     global last_uploaded_file, total_files_downloaded

#     if last_uploaded_file:
#         total_files_downloaded += 1
#         return FileResponse(path=last_uploaded_file, media_type='application/octet-stream', filename=last_uploaded_file)
#     else:
#         total_files_downloaded += 1
#         return FileResponse(path="blynk.bin", media_type='application/octet-stream', filename="blynk.bin")

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
import os

app = FastAPI()

# Variable to store the last uploaded file name
last_uploaded_file = None
# Variable to store the firmware version
firmware_version = "0.0.1"
# Variable to track total files downloaded
total_files_downloaded = 0

uploaded = None

# HTML form for file upload and firmware manipulation
upload_form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Firmware Upload Form</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }}

        .container {{
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}

        h2 {{
            color: #333333;
        }}

        input[type="file"] {{
            margin-bottom: 10px;
        }}

        input[type="submit"] {{
            background-color: #4caf50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}

        input[type="submit"]:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h3>Current Firmware Version: {firmware_version}</h3>
        <h3>Total Files Downloaded: {total_files_downloaded}</h3>

        <h3>Upload Firmware.bin File</h3>
        <form action="/upload_file/" method="post" enctype="multipart/form-data">
            <input type="file" name="file"><br><br>
            <input type="submit" value="Upload">
        </form>

        <h3>Download Last Uploaded File</h3>
        <form action="/get_file/" method="get">
            <input type="submit" value="Download Last Uploaded File">
        </form>
    </div>
</body>
</html>
""".format(firmware_version=firmware_version, total_files_downloaded=total_files_downloaded)


@app.get("/", response_class=HTMLResponse)
async def home():
    return upload_form_html

@app.get("/get_version/")
async def get_version():
    return {"version": firmware_version}

@app.get("/get_size/")
async def get_version():
    return {"Content-Length": str(os.path.getsize("blynk.bin"))}

@app.get("/set_version/")
async def set_version(version: str):
    global firmware_version
    firmware_version = version
    return {"message": "Firmware version set successfully", "version": firmware_version}

@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    global last_uploaded_file, uploaded
    last_uploaded_file = None
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    last_uploaded_file = file.filename
    uploaded = 21
    return {"filename": file.filename}

@app.get("/get_file/")
async def get_file():
    global last_uploaded_file, total_files_downloaded, uploaded
    if uploaded:
        total_files_downloaded += 1
        headers = {
            "Content-Length": str(os.path.getsize(last_uploaded_file)),
            "Content-Disposition": f'attachment; filename={last_uploaded_file}'
        }
        return FileResponse(path=last_uploaded_file, media_type='application/octet-stream', filename=last_uploaded_file, headers=headers)
    elif (uploaded==None):
        total_files_downloaded += 1
        headers = {
            "Content-Length": str(os.path.getsize("blynk.bin")),
            "Content-Disposition": f'attachment; filename={"blynk.bin"}'
        }
        print("FILE SIZE: "+headers["Content-Length"])
        return FileResponse(path="blynk.bin", media_type='application/octet-stream', filename="blynk.bin", headers=headers)
        # return {"message": "No FIle"}
