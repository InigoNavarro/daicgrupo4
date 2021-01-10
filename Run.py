import os

with open ('test.txt', 'r') as f:
	contenido = f.read()
	print(contenido)
	if "True" in contenido:
		os.system("python Grupo4.py True")
	elif "False" in contenido:
		os.system("python Grupo4.py False")
