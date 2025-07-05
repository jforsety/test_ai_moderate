import aiofiles
import uvicorn
import requests
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

DEEPAI_API_KEY = os.getenv('DEEPAI_API_KEY')
URL = os.getenv('URL')
IMAGE_DIR = "images"  # Папка для хранения изображений


class ImageRequest(BaseModel):
    filename: str  # Модель для запроса с именем файла


@app.post("/moderate")
async def moderate(data: ImageRequest):
    # Проверяем расширение файла
    ext = os.path.splitext(data.filename)[1].lower()
    if ext not in [".jpg", ".png"]:
        raise HTTPException(
            status_code=400,
            detail="Поддерживаются только JPG и PNG"
        )

    # Формируем путь к файлу
    file_path = os.path.join(IMAGE_DIR, data.filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Файл не найден"
        )

    try:
        # Асинхронное чтение файла
        async with aiofiles.open(file_path, "rb") as f:
            image_bytes = await f.read()

        # Отправка в DeepAI
        r = requests.post(
            URL,
            files={"image": (data.filename, image_bytes)},
            headers={"api-key": DEEPAI_API_KEY}
        )

        if r.status_code != 200:
            return JSONResponse(
                status_code=502,
                content={"status": "ERROR", "reason": "Ошибка DeepAI"}
            )

        result = r.json()
        nsfw_score = result.get("output", {}).get("nsfw_score", 0)

        if nsfw_score > 0.7:
            return {
                "status": "REJECTED",
                "reason": "Обнаружен NSFW контент",
                "score": float(nsfw_score)  # Добавляем оценку в ответ
            }

        return {"status": "OK", "score": float(nsfw_score)}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "ERROR", "reason": str(e)}
        )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)