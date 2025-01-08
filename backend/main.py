from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create-container")
async def create_container(
        project_name: str = Form(...),
        language: str = Form(...),
        file: Optional[UploadFile] = None
):
    try:
        logger.info(f"Creating container for project: {project_name}")

        project_dir = f"./projects/{project_name}"
        os.makedirs(project_dir, exist_ok=True)
        logger.info(f"Created directory: {project_dir}")

        dockerfile_content = f"FROM {language.lower()}:slim\nWORKDIR /app\n"

        if file:
            logger.info(f"Processing file: {file.filename}")
            file_path = os.path.join(project_dir, file.filename)
            contents = await file.read()

            with open(file_path, "wb") as f:
                f.write(contents)
            logger.info(f"Saved file to: {file_path}")

            dockerfile_content += f"COPY {file.filename} /app/{file.filename}\n"
            dockerfile_content += f'CMD ["{language.lower()}", "/app/{file.filename}"]\n'

        dockerfile_path = os.path.join(project_dir, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        logger.info(f"Created Dockerfile at: {dockerfile_path}")

        image_name = f"{project_name}:latest"
        logger.info(f"Building Docker image: {image_name}")

        try:
            result = subprocess.run(
                ["docker", "build", "-t", image_name, project_dir],
                capture_output=True,
                text=True,
                check=True  # יזרוק שגיאה אם הבנייה נכשלת
            )
            logger.info("Docker build completed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Docker build failed: {e.stderr}")
            raise HTTPException(
                status_code=500,
                detail=f"Docker build failed: {e.stderr}"
            )

        return {
            "message": "Image created successfully!",
            "image_name": image_name
        }

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))