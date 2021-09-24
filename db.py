import pymysql

conn = pymysql.connect(
    host='sql5.freesqldatabase.com',
    database='sql5439612',
    user='sql5439612',
    password='Dau9ADHUtz',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
    )

cursor = conn.cursor()
sql_query = """ CREATE TABLE cliente (
    id int(11) NOT NULL AUTO_INCREMENT,
    nombreComercial varchar(255) NOT NULL,
    razonSocial varchar(255) NOT NULL,
    correoElectronico varchar(255) NOT NULL,
    telefono varchar(255) NOT NULL,
    estado varchar(255) NOT NULL,
    municipio varchar(255) NOT NULL,
    colonia varchar(255) NOT NULL,
    codigoPostal int(11) NOT NULL,
    calle varchar(255) NOT NULL,
    numExt varchar(255) NOT NULL,
    numInt varchar(255) NOT NULL,
    estatus int(11) NOT NULL,
    PRIMARY KEY (id)
    )
    AUTO_INCREMENT=1 ;"""

cursor.execute(sql_query)
conn.close()