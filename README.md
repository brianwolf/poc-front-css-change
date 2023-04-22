# poc-front-change-css

> es una poc de un front que toma el css de un archivo subido en un s3 de minio dependiendo del cliente que este configurado

## Requisitos

* nvm
* node v18
* yarn
* python3.10
* docker
* docker compose

## Pasos

1) Levantar el front

Dentro del proyecto front

```bash
yarn install
yarn start
```

2) Levantar el back

Dentro del proyecto back

```bash
python -m venv env
. env/bin/activate
pip install -r requirements.txt
python app.py
```

3) Levantar minio

Dentro de la carpeta minio

```bash
docker compose up
```

4) Crear un bucket en minio con el nombre de **clientes** y agregarle las carpetas dentro de "clientes"

5) Crear en minio un api token y api secret para configurarlos en el .env del back
