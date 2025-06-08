import boto3
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def subir_archivo(nombre_archivo_local, bucket):
    if not os.path.exists(nombre_archivo_local):
        raise FileNotFoundError(f"Archivo no encontrado: {nombre_archivo_local}")

    s3 = boto3.client('s3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    # Generar nombre remoto con fecha y hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_remoto = f"{timestamp}_{nombre_archivo_local}"

    s3.upload_file(nombre_archivo_local, bucket, nombre_remoto)
