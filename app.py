import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

# Conexión con la base de datos
def db_connectio():
    conn = None
    try:
        conn = pymysql.connect(host='sql5.freesqldatabase.com',
                                database='sql5439612',
                                user='sql5439612',
                                password='Dau9ADHUtz',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor
    )
    except pymysql.Error as e:
        print(e)
    return conn

# Ruta GET para acceder a todos los clientes de la base de datos
# Ruta POST para agreagar un nuevo cliente
@app.route('/clientes', methods=['GET', 'POST'])
def cliente():
    # Traemos la función de la conexion a la base de datos
    conn = db_connectio()
    cursor = conn.cursor()
    
    # Si se recibe una petición GET
    if request.method == 'GET':
        try:
            # Se realiza una consulta para trear todos los datos con estatus 1 (ativo)
            cursor.execute("SELECT * FROM cliente WHERE estatus=1")
            # Se realiza un diccionario para colocar los datos correspodientes en un array de clientes
            clientes = [
                dict(id=row['id'], nombreComercial=row['nombreComercial'], razonSocial=row['razonSocial'],correoElectronico=row['correoElectronico'],telefono=row['telefono'],estado=row['estado'],municipio=row['municipio'],colonia=row['colonia'],codigoPostal=row['codigoPostal'],calle=row['calle'],numExt=row['numExt'],numInt=row['numInt'],estatus=row['estatus'])
                for row in cursor.fetchall()
            ]
            # Se comprueban que el array clientes esta lleno
            if clientes is not None:
                return jsonify(clientes)
        except:
            return f"{-1}"
    
    # Si se recibe una peticion POST        
    if request.method == 'POST':
        # Se toman los datos que se mandan en el request y se asignan a las variables
        try:
            nuevo_nombreComercial = request.form['nombreComercial']
            nuevo_razonSocial = request.form['razonSocial']
            nuevo_correoElectronico = request.form['correoElectronico']
            nuevo_telefono = request.form['telefono']
            nuevo_estado = request.form['estado']
            nuevo_municipio = request.form['municipio']
            nuevo_colonia = request.form['colonia']
            nuevo_codigoPostal = request.form['codigoPostal']
            nuevo_calle = request.form['calle']
            nuevo_numExt = request.form['numExt']
            nuevo_numInt = request.form['numInt']
            estatus = 1
            
            # Se realiza la inserción a la base de datos 
            sql = """INSERT INTO cliente (nombreComercial, razonSocial, correoElectronico,
                                            telefono, estado, municipio,
                                            colonia, codigoPostal, calle,
                                            numExt, numInt, estatus) 
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql, (nuevo_nombreComercial,
                                        nuevo_razonSocial,
                                        nuevo_correoElectronico,
                                        nuevo_telefono,
                                        nuevo_estado,
                                        nuevo_municipio,
                                        nuevo_colonia,
                                        nuevo_codigoPostal,
                                        nuevo_calle,
                                        nuevo_numExt,
                                        nuevo_numInt,
                                        estatus))
            conn.commit()
            return f"{cursor.lastrowid}"
        except:
            return f"{-1}"
        
# Ruta GET para consultar un cliente
# Ruta PUT para actualizar un cliente
# Ruta DELETE para eliminar un cliente cliente    
@app.route('/cliente/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def unico_cliente(id):
    try:
        conn = db_connectio()
        cursor = conn.cursor()
        cliente = None
        # Si recoibe una peteción GET
        if request.method == 'GET':
            # Se realizar consulta a la base de datos donde el estatus sea 1 (activo) y el id coincida con el que se esta recibiendo
            cursor.execute("SELECT * FROM cliente WHERE estatus=1 AND id=%s", (id,))
            rows = cursor.fetchall()
            for r in rows:
                cliente = r
            if cliente is not None:
                return jsonify(cliente), 200
            else:
                return "Algo salio mal", 404
    except:
        return f"{-1}"
    
    try: 
        # Si se recibe una petición PUT
        if request.method == 'PUT':
            # Se realizar una actulización al cliente seleccionado por medio del id 
            sql = """UPDATE cliente
                        SET nombreComercial=%s, 
                            razonSocial=%s, 
                            correoElectronico=%s,
                            telefono=%s, 
                            estado=%s, 
                            municipio=%s,
                            colonia=%s, 
                            codigoPostal=%s, 
                            calle=%s,
                            numExt=%s, 
                            numInt=%s
                        WHERE id=%s"""
            
            # Tomando los datos del request se asigann a las varibles
            nombreComercial = request.form['nombreComercial'] 
            razonSocial = request.form['razonSocial'] 
            correoElectronico = request.form['correoElectronico']
            telefono = request.form['telefono'] 
            estado = request.form['estado']
            municipio = request.form['municipio']
            colonia = request.form['colonia'] 
            codigoPostal = request.form['codigoPostal']
            calle = request.form['calle']
            numExt = request.form['numExt'] 
            numInt = request.form['numInt']
            
            # Se hace un array de asignación del cliente modificado
            actulizar_cliente = {
                "id": id,
                "nombreComercial": nombreComercial,
                "razonSocial": razonSocial,
                "correoElectronico": correoElectronico,
                "telefono": telefono,
                "estado": estado,
                "municipio": municipio,
                "colonia": colonia,
                "codigoPostal": codigoPostal,
                "calle":  calle,
                "numExt": numExt,
                "numInt": numInt
            }
            # Se executa el comando sql y se pasan los datos
            cursor.execute(sql, (nombreComercial, 
                                razonSocial, 
                                correoElectronico, 
                                telefono, 
                                estado, 
                                municipio, 
                                colonia, 
                                codigoPostal, 
                                calle, 
                                numExt, 
                                numInt, 
                                id,))
            conn.commit()
            return jsonify(actulizar_cliente)
    except:
        return f"{-1}"    
    
    try:
        # se recibe una petición DELETE
        if request.method == 'DELETE':
            # Se realizar una actulización al cliente seleccionado por medio del id
            # Se modifica el estatus 0 (desactivado)
            sql = """UPDATE cliente
                        SET estatus=%s
                        WHERE id=%s"""
            cursor.execute(sql, (0, id))
            conn.commit()
            
            return f"{1}"              
    except:
        return f"{-1}"
                
                
if __name__ == '__main__':
    app.run()