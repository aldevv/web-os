# No es funcional en windows, solo con ubuntu usando WSL
# Dependencias
```
sudo apt-get install make python3 python3-dev python3-venv
```

# Instrucciones
## Crear ambiente virtual
Entrar en la carpeta chmaquina y correr este comando
```bash
python3 -m venv env
```
## activar el ambiente virtual 
En la carpeta chmaquina correr el siguiente comando
```bash
source env/bin/activate
```
## Instalar requerimientos
### Windows con WSL
```bash
pip install wheel && pip install -r requirements.txt
```
### Linux
```bash
pip install -r requirements.txt
```
## Preparar el frontend
Usar un live-server, la extension de vscode llamada live server puede ser utilizada para correr el index.html en la carpeta frontend.
en el caso de live-server de vscode, la pagina queda disponible en el browser en el puerto 5500, solo es poner en la url el siguiente path 

localhost:5500

## Correr el servidor
finalmente ir a la carpeta backend y correr 
```bash
gunicorn run:api --worker-class gevent
```
