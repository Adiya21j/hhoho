import boto3
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

# Variable to store the firmware version
firmware_version = "0.0.1"
# Variable to track total files downloaded
total_files_downloaded = 0

# S3 setup
s3 = boto3.client('s3')
bucket_name = 'your-bucket-name'

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

@app.get("/set_version/")
async def set_version(version: str):
    global firmware_version
    firmware_version = version
    return {"message": "Firmware version set successfully", "version": firmware_version}

@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    global total_files_downloaded
    s3.upload_fileobj(file.file, bucket_name, file.filename)
    total_files_downloaded += 1
    return {"filename": file.filename}

@app.get("/get_file/")
async def get_file():
    global total_files_downloaded
    total_files_downloaded += 1
    # Here you would return the file from S3 or any other storage location
    # Replace this with the appropriate S3 download code
    # For example:
    s3.download_file(bucket_name, key, '/tmp/file_to_return')
    return FileResponse(path="/tmp/file_to_return", media_type='application/octet-stream', filename=file.filename)
    # return FileResponse(path="blynk.bin", media_type='application/octet-stream', filename="blynk.bin")
