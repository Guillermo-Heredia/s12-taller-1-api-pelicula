import boto3
import uuid
import os
import json


def imprimir_log(tipo, log_datos):

    log = {
        "tipo": tipo,
        "log_datos": log_datos
    }
    print(json.dumps(log, ensure_ascii=False, default=str))


def lambda_handler(event, context):
    try:
        # Entrada (JSON)
        # API Gateway puede enviar body como diccionario o como string JSON.
        body = event.get("body", {})

        if isinstance(body, str):
            body = json.loads(body)

        tenant_id = body["tenant_id"]
        pelicula_datos = body["pelicula_datos"]
        nombre_tabla = os.environ["TABLE_NAME"]

        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            "tenant_id": tenant_id,
            "uuid": uuidv4,
            "pelicula_datos": pelicula_datos
        }

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log de ejecución correcta
        imprimir_log("INFO", {
            "mensaje": "Película creada correctamente",
            "pelicula": pelicula
        })

        # Salida (JSON)
        return {
            "statusCode": 200,
            "pelicula": pelicula,
            "response": response
        }

    except Exception as e:
        # Log de error con el mismo formato JSON estándar
        imprimir_log("ERROR", {
            "mensaje": "Error al crear la película",
            "tipo_error": type(e).__name__,
            "error": str(e)
        })

        return {
            "statusCode": 500,
            "body": json.dumps({
                "mensaje": "Error al crear la película",
                "tipo_error": type(e).__name__
            }, ensure_ascii=False)
        }
