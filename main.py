from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas  # Importar los esquemas desde schemas.py

app = FastAPI()

host_name = "100.27.62.167"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_licencias"

# Conectar a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host=host_name,
        port=port_number,
        user=user_name,
        password=password_db,
        database=database_name
    )

# Crear una nueva licencia
@app.post("/licencias")
def create_licencia(licencia: schemas.Licencia):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    sql = "INSERT INTO licencia (conductor_id, tipo, fecha_expedicion, fecha_expiracion, numero) VALUES (%s, %s, %s, %s, %s)"
    val = (licencia.conductor_id, licencia.tipo, licencia.fecha_expedicion, licencia.fecha_expiracion, licencia.numero)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Licencia creada con éxito"}

# Consultar una licencia por ID
@app.get("/licencias/{id}")
def get_licencia(id: int):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM licencia WHERE id = %s", (id,))
    result = cursor.fetchone()
    mydb.close()
    if result:
        return {"licencia": result}
    else:
        raise HTTPException(status_code=404, detail="Licencia no encontrada")

# Renovar una licencia (actualizar fecha de expiración)
@app.put("/licencias/{id}")
def renovar_licencia(id: int, licencia: schemas.LicenciaUpdate):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    sql = "UPDATE licencia SET fecha_expiracion = %s WHERE id = %s"
    val = (licencia.fecha_expiracion, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Licencia renovada con éxito"}

# Revocar una licencia (eliminar)
@app.delete("/licencias/{id}")
def revocar_licencia(id: int):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM licencia WHERE id = %s", (id,))
    mydb.commit()
    mydb.close()
    return {"message": "Licencia revocada con éxito"}