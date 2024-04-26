from app import create_app
import uvicorn

# Create a FASTAPI instance
app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
