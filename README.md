# Instrucciones
## instalar python
```bash
sudo apt-get install python3
```
## Crear ambiente virtual
```bash
python3 -m venv env
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
## activar el ambiente virtual 
```bash
source env/bin/activate
```
## Correr el servidor
ir a la carpeta backend y correr 
```bash
gunicorn run:api --worker-class gevent
```
### Abrir interfaz grafica
abrir index.html en la carpeta frontend 
