from fastapi import FastAPI, Form, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# FastAPI app initialization
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Chat history storage
messages = [{"role": "system", "content": "You are a helpful AI assistant."}]


def encode_image(image_path):
    """Encodes an image as base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the homepage."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chatbot/", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    """Render the chatbot page."""
    return templates.TemplateResponse("chatbot.html", {"request": request})


@app.post("/chat/")
async def chatbot_response(
    user_input: str = Form(...),
    image: UploadFile = None,
):
    """Handle user input and return chatbot's response."""
    global messages

    # Prepare the content for the chatbot
    content = []
    if user_input.strip():
        content.append({"type": "text", "text": user_input})

    if image and image.filename:  # Check if an image was uploaded
        try:
            # Ensure the uploads directory exists
            os.makedirs("uploads", exist_ok=True)
            
            # Save and encode the image
            image_path = f"uploads/{image.filename}"
            with open(image_path, "wb") as f:
                f.write(await image.read())
            base64_image = encode_image(image_path)
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

    # Add user content to the chat history
    messages.append({"role": "user", "content": content})

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            stream=True
        )

        full_response = ""
        for chunk in response:
            # Access the content directly
            if chunk.choices[0].delta and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content

        # Add the assistant's response to the chat history
        messages.append({"role": "assistant", "content": full_response})
        return {"response": full_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
