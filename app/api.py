# from http.server import BaseHTTPRequestHandler, HTTPServer
# import os
# import re

# # Define the directory to save uploaded .bin files
# UPLOAD_DIRECTORY = "uploaded_files"

# # Initialize firmware version
# FIRMWARE_VERSION = "1.0.0"

# # Initialize download counter
# DOWNLOAD_COUNTER = 0

# # HTML template for the file upload form
# UPLOAD_FORM_HTML = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Upload .bin File</title>
#     <style>
#         body {{
#             font-family: Arial, sans-serif;
#         }}
#         form {{
#             margin-top: 20px;
#         }}
#         input[type="submit"] {{
#             padding: 10px 20px;
#             background-color: #007bff;
#             color: #fff;
#             border: none;
#             cursor: pointer;
#         }}
#         .yellow-btn {{
#             padding: 10px 20px;
#             background-color: #ffc107;
#             color: #fff;
#             border: none;
#             cursor: pointer;
#         }}
#         .green-btn {{
#             padding: 10px 20px;
#             background-color: #28a745;
#             color: #fff;
#             border: none;
#             cursor: pointer;
#         }}
#     </style>
# </head>
# <body>
#     <h1>Upload .bin File</h1>
#     <form action="/upload" method="post" enctype="multipart/form-data">
#         <input type="file" name="file">
#         <input type="submit" value="Upload">
#     </form>
#     <h2>Update Firmware Version</h2>
#     <form action="/update_version" method="post">
#         <input type="text" name="version" placeholder="Enter new version">
#         <input type="submit" value="Update Version">
#     </form>
#     <h2>Actions</h2>
#     <button class="yellow-btn" onclick="getFirmwareVersion()">Get Firmware Version</button>
#     <button class="green-btn" onclick="downloadBinFile()">Download .bin File</button>
#     <p>Download Count: <span id="downloadCount">{}</span></p>
#     <script>
#         function getFirmwareVersion() {{
#             fetch('/version')
#             .then(response => response.text())
#             .then(data => alert('Current Firmware Version: ' + data))
#             .catch(error => console.error('Error:', error));
#         }}
        
#         function downloadBinFile() {{
#             fetch('/download')
#             .then(response => {{
#                 if (response.ok) {{
#                     document.getElementById('downloadCount').innerText = parseInt(document.getElementById('downloadCount').innerText) + 1;
#                     return response.blob();
#                 }}
#                 throw new Error('Network response was not ok.');
#             }})
#             .then(blob => {{
#                 const url = window.URL.createObjectURL(blob);
#                 const a = document.createElement('a');
#                 a.href = url;
#                 a.download = 'uploaded.bin';
#                 document.body.appendChild(a);
#                 a.click();
#                 window.URL.revokeObjectURL(url);
#             }})
#             .catch(error => console.error('Error:', error));
#         }}
#     </script>
# </body>
# </html>
# """.format(DOWNLOAD_COUNTER)

# class RequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(UPLOAD_FORM_HTML.encode())
#         elif self.path == '/version':
#             self.send_response(200)
#             self.send_header('Content-type', 'text/plain')
#             self.end_headers()
#             self.wfile.write(FIRMWARE_VERSION.encode())
#         elif self.path == '/download':
#             global DOWNLOAD_COUNTER
#             DOWNLOAD_COUNTER += 1
#             self.send_response(200)
#             self.send_header('Content-type', 'application/octet-stream')
#             self.send_header('Content-Disposition', 'attachment; filename=uploaded.bin')
#             self.end_headers()
#             with open(os.path.join(UPLOAD_DIRECTORY, 'uploaded.bin'), 'rb') as f:
#                 self.wfile.write(f.read())
#         else:
#             self.send_error(404, "File not found")
#         return

#     def do_POST(self):
#         if self.path == '/upload':
#             content_length = int(self.headers['Content-Length'])
#             uploaded_file = self.rfile.read(content_length)
#             filename = os.path.join(UPLOAD_DIRECTORY, 'uploaded.bin')
#             with open(filename, 'wb') as f:
#                 f.write(uploaded_file)

#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write("File uploaded successfully.".encode())
#         elif self.path == '/update_version':
#             content_length = int(self.headers['Content-Length'])
#             post_data = self.rfile.read(content_length).decode('utf-8')
#             new_version = re.search(r'version=(.*)', post_data).group(1)
#             global FIRMWARE_VERSION
#             FIRMWARE_VERSION = new_version
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write("Firmware version updated successfully.".encode())
#         else:
#             self.send_error(404, "File not found")
#         return

# def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#     print(f"Server started on port {port}")
#     httpd.serve_forever()
#     return 

# # if __name__ == "__main__":
# #     if not os.path.exists(UPLOAD_DIRECTORY):
# #         os.makedirs(UPLOAD_DIRECTORY)
# #     run()
# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import HTMLResponse

# app = FastAPI()

# # Variable to store the last uploaded file name
# last_uploaded_file = None

# # Dummy firmware version
# firmware_version = "0.0.1"

# # HTML form for file upload
# upload_form_html = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>File Upload Form</title>
# </head>
# <body>
#     <h2>Upload a .bin file</h2>
#     <form action="/uploadfile/" method="post" enctype="multipart/form-data">
#         <input type="file" name="file"><br><br>
#         <input type="submit" value="Upload">
#     </form>
# </body>
# </html>
# """

# @app.get("/", response_class=HTMLResponse)
# async def home():
#     return upload_form_html

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     global last_uploaded_file
#     with open(file.filename, "wb") as buffer:
#         buffer.write(file.file.read())
#     last_uploaded_file = file.filename
#     return {"filename": file.filename}

# @app.get("/firmware/version")
# async def get_firmware_version():
#     return {"version": firmware_version}

# @app.post("/firmware/version")
# async def set_firmware_version(version: str):
#     global firmware_version
#     firmware_version = version
#     return {"message": "Firmware version set successfully", "version": firmware_version}

# @app.get("/downloadfile/")
# async def download_file():
#     global last_uploaded_file
#     if last_uploaded_file:
#         return FileResponse(path=last_uploaded_file, media_type='application/octet-stream', filename=last_uploaded_file)
#     else:
#         return {"error": "No file has been uploaded yet"}

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Variable to store the last uploaded file name
last_uploaded_file = None
# Variable to store the firmware version
firmware_version = "0.0.1"
# Variable to track total files downloaded
total_files_downloaded = 0

# HTML form for file upload and firmware manipulation
upload_form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>File Upload Form</title>
</head>
<body>
    <h2>Current Firmware Version</h2>
    <p>{firmware_version}</p>
    <h2>Total Files Downloaded</h2>
    <p>{total_files_downloaded}</p>

    <h2>Upload firmware.bin file</h2>
    <form action="/upload_file/" method="post" enctype="multipart/form-data">
        <input type="file" name="file"><br><br>
        <input type="submit" value="Upload">
    </form>

    <h2>Download last uploaded file</h2>
    <form action="/get_file/" method="get">
        <input type="submit" value="Download Last Uploaded File">
    </form>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return upload_form_html.format(firmware_version=firmware_version, total_files_downloaded=total_files_downloaded)

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
    global last_uploaded_file
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    last_uploaded_file = file.filename
    return {"filename": file.filename}

@app.get("/get_file/")
async def get_file():
    global last_uploaded_file, total_files_downloaded
    if last_uploaded_file:
        total_files_downloaded += 1
        return FileResponse(path=last_uploaded_file, media_type='application/octet-stream', filename=last_uploaded_file)
    else:
        return {"error": "No file has been uploaded yet"}
