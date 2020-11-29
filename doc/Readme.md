# Documentación

**Nombre** | **Grupo** | **Github**
--|--|--
Dalianys Pérez Perera | C411 | [@DalyPerez](https://github.com/DalyPerez)
Dayany Alfaro González | C411 | [@dayanyalfaro](https://github.com/dayanyalfaro)
Gilberto González Rodríguez | C411 | [@ginrod](https://github.com/ginrod)

# Uso del compilador

Para usar el compilador es necesario tener instalado Python 3.7 o superior. Como requisito está el paquete **ply** el cual puede ser instalado usando pip. Si se quiere hacer uso de los tests automáticos además de PLY es necesario instalar **pytest** y **pytest-ordering**. Todos los requerimientos pueden ser instalados ejecutando **python -m pip install -r requeriments.txt** desde la raíz del proyecto. El módulo que contiene toda la lógica del compilador es **cil_to_mips.py**. Para utilizarlo el path relativo a **cil_to_mips.py** o un path absoluto de un fichero con código fuente de COOL se debe pasar como argumento al módulo, por ejemplo, ejecutar **python cil\_to\_mips.py <path>**. Un archivo en el mismo path del código fuente será creado, con el mismo nombre, pero con extensión .mips. Este fichero contendrá código MIPS con pseudo instrucciones y se puede probar en cualquier implementación del simulador SPIM, como por ejemplo, QtSpim.