import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS  # Import configurations
from utils.logger import logger  # Assuming a logger is set up in utils/logger.py

app = FastAPI()

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_allowed_file(filename: str) -> bool:
    """Validate file extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/upload/")
async def upload_file(file: UploadFile):
    """Handle file upload and save it to the upload folder."""
    # Validate file extension
    if not is_allowed_file(file.filename):
        logger.warning(f"Upload failed: Unsupported file type - {file.filename}")
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Define the file path
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        # Save the file to the upload folder
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        logger.info(f"File uploaded successfully: {file.filename}")
        return JSONResponse(content={"filename": file.filename, "status": "uploaded"}, status_code=200)
    
    except Exception as e:
        logger.error(f"File upload failed: {file.filename} - Error: {str(e)}")
        raise HTTPException(status_code=500, detail="File upload failed")
