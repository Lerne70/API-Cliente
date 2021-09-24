import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

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

@app.route('/clientes', methods=['GET', 'POST'])
def cliente():
    conn = db_connectio()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM cliente WHERE estatus=1")
        
        clientes = [
            dict(id=row['id'], nombreComercial=row['nombreComercial'], razonSocial=row['razonSocial'],correoElectronico=row['correoElectronico'],telefono=row['telefono'],estado=row['estado'],municipio=row['municipio'],colonia=row['colonia'],codigoPostal=row['codigoPostal'],calle=row['calle'],numExt=row['numExt'],numInt=row['numInt'],estatus=row['estatus'])
            for row in cursor.fetchall()
        ]
        if clientes is not None:
            return jsonify(clientes)
            
    if request.method == 'POST':
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
        
    
@app.route('/cliente/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def unico_cliente(id):
    conn = db_connectio()
    cursor = conn.cursor()
    cliente = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM cliente WHERE id=%s", (id,))
        rows = cursor.fetchall()
        for r in rows:
            cliente = r
        if cliente is not None:
            return jsonify(cliente), 200
        else:
            return "Algo salio mal", 404
        
    if request.method == 'PUT':
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
    
    if request.method == 'DELETE':
        sql = """UPDATE cliente
                    SET estatus=%s
                    WHERE id=%s"""
        cursor.execute(sql, (0, id))
        conn.commit()
        
        return f"{1}"              
                
                
                
if __name__ == '__main__':
    app.run()