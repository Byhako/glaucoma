from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import uvicorn
import io

from load_models import load_models
from predict import predict

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes. Puedes especificar dominios específicos en lugar de "*"
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

# Cargar los modelos
models = load_models()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), model: str = "mobilenet"):
    content = await file.read()
    image = Image.open(io.BytesIO(content))

    # Analizar la imagen
    predicted_label, value_confidence = predict(image, models[model])

    value_confidence = round(value_confidence * 100, 2)

    response_data = {
        "message": f"{predicted_label} tienes glaucoma con un {value_confidence}% de confianza."
    }

    return JSONResponse(content=response_data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
