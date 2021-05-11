# Documentación

**Nombre** | **Grupo** | **Github**
--|--|--
Carlos Bermudez Porto | C412 | [@cbermudez97](https://github.com/cbermudez97)
Leynier Gutiérrez González | C412 | [@leynier](https://github.com/leynier)
Tony Raúl Blanco Fernández | C411 | [@70nybl4nc0](https://github.com/70nybl4nc0)

## Uso

Para instalar las dependencias deberá correr en la terminal el comando:

```bash
pip install -r requirements.txt
```

Para ejecutar el compilador se deberá correr en la terminal el comando:

```bash
python coolc.py <INPUT_FILE.cl> <OUTPUT_FILE.mips>
```

Adicionalmente se le pueden adicionar al compilador diferentes argumentos opcionales. Estos argumentos son los siguientes:

* --cil: Este argumento indica al compilador que se desea generar un archivo con el código CIL generado en las etapas intermedias del proceso de compilación.
* --verbose: Estos argumentos opcionales indican al compilador que se desea ejecutar el mismo en modo verboso. El modo verboso agrega a la salida estándar del compilador información adicional. La estructura del ast de COOL generado y datos sobre los tipos definidos en el código son parte de esta información adicional.
* --help: Estos argumentos mostrarán una ayuda mínima referente al uso del comando, así como de los demás argumentos opcionales del mismo.
