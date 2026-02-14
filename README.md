# Asistente de Derivación Legal - Proyecto AI Engineering

Este proyecto es una utilidad de procesamiento de texto diseñada para actuar como un asistente de triaje legal inteligente.

El sistema recibe consultas de usuarios sobre diversos conflictos legales y devuelve una respuesta estructurada en formato JSON, clasificando la rama del derecho, sugiriendo el especialista adecuado y recomendando acciones inmediatas.

##  Objetivos del Proyecto
- **Salida Estructurada**: Garantizar respuestas en JSON válido para integraciones posteriores.
- **Monitoreo de Costos**: Registrar latencia, uso de tokens y costo estimado por cada consulta.
- **Ingeniería de Prompts**: Implementación de técnicas de Few-Shot Prompting para asegurar precisión y tono profesional.
- **Seguridad**: Capa de moderación proactiva mediante la API de OpenAI.

##  Estructura del Repositorio
- **src/**: Contiene la lógica principal (run_query.py) y el módulo de seguridad (safety.py).
- **prompts/**: Plantilla del prompt principal con instrucciones y ejemplos Few-Shot.
- **metrics/**: Archivos JSON con el registro histórico de latencia, tokens y costos.
- **tests/**: Pruebas unitarias para validar el contrato de datos y cálculos.
- **reports/**: Informe técnico detallado de la arquitectura y decisiones.

##  Configuración e Instalación

1. **Requisitos previos**: Se recomienda el uso de **uv** para la gestión de dependencias.
2. **Entorno Virtual**: Crea y activa tu entorno para mantener las dependencias aisladas.
   - Ejecutar: `uv venv`
   - Activar (Windows): `source .venv/Scripts/activate`
   - Activar (Unix/Mac): `source .venv/bin/activate`
3. **Instalación de dependencias**:
   - Ejecutar: `uv pip install -r requirements.txt`
4. **Variables de Entorno**: Crea un archivo **.env** en la raíz del proyecto y añade tu API Key:
   - `OPENAI_API_KEY=tu_clave_aqui`

##  Ejecución
Para procesar una consulta legal de prueba y ver el resultado en consola, ejecuta:
```bash
python src/run_query.py
```

## El proyecto incluye validaciones automáticas para asegurar que la IA siempre devuelva los campos requeridos:
python -m pytest

#  Seguridad y Moderación 
El asistente utiliza el endpoint de Moderación de OpenAI en el módulo safety.py. Este componente analiza la intención del usuario antes de procesar la consulta legal. Si se detecta contenido relacionado con violencia, odio o acoso, la solicitud se detiene automáticamente para proteger el sistema y optimizar el consumo de tokens.