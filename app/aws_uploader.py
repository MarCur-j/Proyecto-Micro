import boto3
import os
from dotenv import load_dotenv
load_dotenv()

def subir_archivo(nombre_archivo, bucket, nombre_remoto):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )
    s3.upload_file(nombre_archivo, bucket, nombre_remoto)
