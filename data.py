from ctypes.wintypes import HWINSTA
from distutils import archive_util
import psycopg2
import psycopg2.extras
from PyPDF2 import PdfFileReader
from subprocess import Popen
import subprocess
import os
from subprocess import check_output

hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = 'admin'
port_id = 5432

conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id)

cur=conn.cursor()

#print(cur)

print("¿Nome de documento?")
nombre = input()
extension = ".pdf"
archivo = f"{nombre}{extension}"
print("¿Si su documento posee clave escribala aqui?")
clave = input()

with open(archivo, "rb") as file:
	pdf = PdfFileReader(file)
	if pdf.isEncrypted:
			pdf.decrypt(clave)
	info = pdf.getDocumentInfo()

a="select * from proyecto_pdf where producer ='"

b=info.producer
d="'"
c=f"{a}{b}{d}"
#print(c)
cur.execute(c)
pru=cur.fetchall()
print(pru)
pru2=pru[0]

a_2="select respuesta from pdf_hints where emisor='"
b_2=pru2[1]
c_2="' and tipo_documento='"
d_2=pru2[2]
e_2="'"
f_2=f"{a_2}{b_2}{c_2}{d_2}{e_2}"
#print(f_2)
cur.execute(f_2)
hint=cur.fetchall()
print(hint)
hint_respuesta=(hint[0])
hint_respuesta=str(hint_respuesta[0])

#qpdf --qdf --object-streams=disable "Bci0021ff7 (1).Pdf" --password=20167824 bci_1.pdf
clave_qpdf="--password="
clave_qpdf_2 = f"{clave_qpdf}{clave}"
a="'"
b=archivo
c="'"
d=f"{a}{b}{c}"
print(clave_qpdf_2)
print(d)
cmd=["qpdf","--qdf", "--object-streams=disable",archivo,clave_qpdf_2,"prueba_1.pdf"]
p = subprocess.Popen(cmd)
p.wait()
#mutool show cartola_3.pdf 10
cmd_2=["mutool","show","prueba_1.pdf","10"]
p = subprocess.Popen(cmd_2)
p.wait()
out = check_output(cmd_2)
src_str = str(out)
print(src_str)
x=src_str[2:]
x=x[:-1]
x = x.replace("n", " ")
x = x.replace('\ ', ' ')
print(x)
print(hint_respuesta)
sub_index = x.find(hint_respuesta)
#print(out[2])
print(sub_index)
#print(x)