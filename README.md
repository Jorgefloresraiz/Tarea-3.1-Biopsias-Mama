# Tarea 3.1: diagnóstico de biopsias

## Archivos
- App_Diagnostico_Biopsias_Mama.ipynb: copia idéntica del cuaderno ejecutado en Colab; no se editaron celdas ni salidas.
- app_biopsias.py: funciones extraídas mediante AST; no entrena ni guarda modelos al importarse.
- test_app.py: cinco funciones de prueba, ocho casos por parametrización.
- evidencia_pytest.txt: salida real de pytest; ocho casos aprobados.
- Informe_Tarea_3_1.pdf: informe técnico de tres páginas para revisión del estudiante.

## Reproducción local
Desde esta carpeta:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v test_app.py
```
El entorno usado aquí hereda los paquetes científicos del Python local; pytest se instaló en .venv. requirements.txt sirve para un entorno nuevo, sin fijar versiones. Las versiones de prueba se registran en evidencia_pytest.txt.

## Colab
Subir el notebook y ejecutar todas las celdas en una sesión nueva. Para las pruebas, subir también app_biopsias.py y test_app.py a la carpeta de trabajo y ejecutar en una celda `!python -m pytest -v test_app.py`.

## Evidencia y límites
Las métricas guardadas en Colab son 1.0000 con fuga, 0.7413 sin fuga y 0.7413 sin fuga con balanced. No se volvió a ejecutar ni modificar el notebook durante la preparación de estos archivos. Las pruebas sí se ejecutaron localmente. Verifican las funciones extraídas, no los gráficos ni la serialización del modelo. La extracción conserva la lógica de las funciones; futuras modificaciones del notebook requieren sincronizar el módulo.

El generador aleatorio global avanza en cada carga: para reproducir el notebook, reiniciar y ejecutar todo una vez. Las pruebas reinician la semilla antes de cargar datos. El accuracy igual con balanced no demuestra iguales errores por clase ni una mejora clínica.

## Historial y entrega
Autor: Jorge Flores Gonzalez. El historial se organizó retrospectivamente por cambios a partir del trabajo en Colab; consultar HISTORIAL.md. El notebook final no fue modificado y su checksum consta en sha256_notebook.txt.

Repositorio de entrega: https://github.com/Jorgefloresraiz/Tarea-3.1-Biopsias-Mama

Entregar el enlace y el PDF en el campus. Conservar las capturas originales como evidencia adicional. No subir .venv ni archivos de modelo.
