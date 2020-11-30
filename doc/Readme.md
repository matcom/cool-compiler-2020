# Documentación

> La siguiente tabla contiene los datos del equipo:

**Nombre** | **Grupo** | **Github**
--|--|--
Oscar Luis Hernandez Solano | C411 | [@oschdez97](https://github.com/oschdez97)
Harold Rosales Hernandez | C411 | [@hros18](https://github.com/hros18)
Carlos Rafael Ortega Lezcano | C411 | [@CRafa97](https://github.com/CRafa97)

## Uso del Compilador

Para instalar todas las dependencias del compilador ejecute desde el directorio raiz del proyecto

```bash
pip install -r requirements.txt
```

Para ejecutar el compilador debe moverse al directorio ```src```, y ejecutar el archivo ```cool.sh``` dando como entrada la direccion del archivo a compilar

```bash
cd src/
./cool.sh '../tests/codegen/hello_world.cl'
```

En caso que no tenga `bash` puede ejecutar directamente el script `main.py` que contiene el proceso de compilacion mediante el pipeline

```bash
python3 main.py '../tests/codegen/hello_world.cl'
```