# 🗺️ Hoja de Ruta: AI Engineering Final Project

## 🎯 Objetivo
Construir un asistente de soporte técnico que reciba consultas, use un prompt estructurado (Few-shot) y devuelva un JSON con métricas de latencia y costo.

---

## 🛠️ Fase 1: Setup Moderno (Herramientas & Estructura)
- [x] Instalación de `uv` y creación del entorno virtual.
- [x] Estructura de carpetas según la consigna.
- [x] Configuración de variables de entorno (`.env`) y `.gitignore`.
- [x] Instalación de dependencias iniciales (`openai`, `python-dotenv`, `pytest`).

## 🧠 Fase 2: Ingeniería de Prompts (El Corazón)
- [ ] Diseño del `main_prompt.txt`.
- [ ] Implementación de técnica **Few-Shot** (ejemplos de entrada/salida).
- [ ] Definición del esquema JSON de respuesta (Strict Output).

## 💻 Fase 3: Desarrollo del Script Core (`src/run_query.py`)
- [ ] Configuración del cliente OpenAI.
- [ ] Función de llamada a la API con manejo de errores.
- [ ] **Módulo de Métricas**: 
    - Cálculo de tokens (prompt vs completion).
    - Medición de latencia (time).
    - Cálculo de costo estimado (USD).

## 📊 Fase 4: Persistencia y Formato
- [ ] Guardado automático de métricas en `metrics/metrics.json`.
- [ ] Formateo de la salida por consola en JSON válido.

## 🛡️ Fase 5: Seguridad y Testing (Bonus)
- [ ] `src/safety.py`: Filtro básico de moderación o palabras prohibidas.
- [ ] `tests/test_core.py`: Validar que la respuesta sea un JSON y que los tokens sean > 0.

## 📝 Fase 6: Entrega y Documentación
- [ ] Creación del `README.md` (Instrucciones de ejecución).
- [ ] Redacción del `PI_report_en.md` (Análisis técnico y arquitectura).
- [ ] Verificación de repositorio autocontenido.


