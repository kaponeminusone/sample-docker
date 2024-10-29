from fastapi import FastAPI, UploadFile, File
import subprocess
import os

app = FastAPI()

OUTPUT_DIR = "pdf_output"

# Crear el directorio de salida si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/convert/")
async def convert_tex(file: UploadFile = File(...)):
    # Guardar el archivo .tex recibido
    tex_file_path = f"/app/{file.filename}"
    with open(tex_file_path, "wb") as f:
        f.write(await file.read())
    
    # Ejecutar pdflatex para convertir el archivo .tex a .pdf
    try:
        subprocess.run(
            ['pdflatex', '-interaction=batchmode', '-output-directory', OUTPUT_DIR, tex_file_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        return {"error": "Error al procesar el archivo .tex"}

    # Definir la ruta del archivo PDF generado
    pdf_file_path = os.path.join(OUTPUT_DIR, file.filename.replace(".tex", ".pdf"))

    # Verificar si el archivo PDF fue creado
    if os.path.exists(pdf_file_path):
        return {"pdf_file": pdf_file_path}
    else:
        return {"error": "No se pudo generar el archivo PDF"}
