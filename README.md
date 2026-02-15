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
4. **Variables de Entorno**: Crea un archivo **.env** en la raíz del proyecto y añade tus API Key:
   - `OPENAI_API_KEY=tu_clave_aqui`
   - `GROQ_API_KEY=your_api_key_here`

##  Ejecución

Para procesar una consulta legal de prueba y ver el resultado en consola, ejecuta:
```bash
python src/run_query.py
```

## El proyecto incluye validaciones automáticas para asegurar que la IA siempre devuelva los campos requeridos:
```bash
python -m pytest
```

## Seguridad y Moderación 
El asistente integra una Capa de Auditoría de Seguridad mediante el endpoint de Moderación de OpenAI en el módulo safety.py.

A diferencia de los filtros estándar, este sistema implementa una moderación no bloqueante:

* **Análisis en tiempo real:** Evalúa categorías sensibles como violencia, odio o acoso.
* **Auditoría Informativa:** El sistema procesa la consulta y etiqueta el resultado en el campo `safety_audit`. Esto permite asistir en casos complejos (como accidentes o disputas) sin interrumpir el flujo, manteniendo un registro de seguridad para el profesional.
* **Persistencia:** Cada auditoría se guarda junto a la respuesta legal en el historial de métricas para optimizar el control del sistema.

## Arquitectura Multi-Agente y Triage de Costo Cero
El sistema implementa una estrategia de **triage legal inteligente** utilizando una arquitectura de dos capas:
* **Filtro de Mérito (Groq + Llama 3.3):** Todas las consultas pasan primero por un agente de bajo costo que determina si el caso requiere realmente asesoría legal. Consultas triviales o fuera de contexto son resueltas en milisegundos sin incurrir en costos de API.
* **Agente Especialista (OpenAI + GPT-4o-mini):** Solo las consultas validadas como "asuntos legales" son derivadas al modelo especialista para su clasificación detallada y recomendación de acciones.
* **Observabilidad Total:** Cada respuesta incluye el campo `llm_used` en sus métricas, permitiendo auditar qué modelo respondió y visualizar el ahorro económico generado por el filtrado preventivo.