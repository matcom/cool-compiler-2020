# Documentación

**Nombre** | **Grupo** | **Github**
--|--|--
Loraine Monteagudo García | C411 | [@lorainemg](https://github.com/lorainemg)
Amanda Marrero Santos | C411 | [@amymsantos42](https://github.com/amymsantos42)
Manuel S. Fernández Arias | C411 | [@nolyfdezarias](https://github.com/nolyfdezarias)

## Uso del compilador

Para el uso del compilador es necesario tener Python 3.7 o superior. Se hace uso de los paquetes `ply` para la generación del lexer y el parser y de `pytest` y `pytest-ordering` para la ejecución de los tests automáticos. Todos los paquetes mencionados pueden ser instalados usando pip ejecutando `pip install -r requirements.txt` en la raíz del proyecto. El archivo principal es `main.py`, ubicado en la carpeta `src`, y recibe como argumento 2 ficheros: uno de entrada que debe tener la extensión `.cl` con el código en COOL y otro de salida que será en donde se guardará el código MIPS generado. También se puede ejecutar el compilador haciendo uso del archivo `coolc.sh`, ubicado también en `src`, que espera como parámetro el programa en COOL. El fichero de MIPS generado por el compilador tendrá el mismo nombre que el fichero de entrada y será ubicado en la misma carpeta, pero tendrá la extensión `.mips`. Este fichero puede ser ejecutado por el simulador de MIPS `spim`.
