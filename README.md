# UIResearch 🔬

<div align="center">

![UIResearch Logo](app/static/favicon.svg)

**Herramienta profesional para búsqueda de referencias académicas**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Demo](http://localhost:8000) • [Documentación](http://localhost:8000/static/docs.html) • [API](http://localhost:8000/docs)

</div>

## 📋 Descripción

UIResearch es una aplicación web moderna para buscar, filtrar y exportar referencias académicas desde la API de Crossref. Diseñada para investigadores, estudiantes y profesionales que necesitan acceso rápido a millones de publicaciones científicas.

### ✨ Características principales

- 🔍 **Búsqueda avanzada** - Busca en millones de artículos académicos
- 🎯 **Filtros inteligentes** - Por fecha, tipo de contenido, presencia de abstract
- 📊 **Exportación múltiple** - CSV y BibTeX
- 🎨 **Interfaz moderna** - Diseño profesional y responsive
- ⚡ **API REST completa** - Integración fácil con otras herramientas
- 📈 **Métricas Prometheus** - Monitoreo y observabilidad
- 🔒 **Rate limiting** - Protección contra abuso

## 🚀 Inicio rápido

### Requisitos previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/inginddie/uiresearch.git
cd uiresearch
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**

Crea un archivo `.env` en la raíz del proyecto:

```env
# Crossref Configuration
APP_USER_AGENT=UIResearch/1.0
APP_MAILTO=tu-email@example.com

# Server Configuration
PORT=8000
LOG_LEVEL=INFO

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:8000

# Rate Limiting
RATE_LIMIT_SEARCHES=10/minute
RATE_LIMIT_EXPORTS=5/minute

# Crossref Client
CROSSREF_TIMEOUT=30
MAX_RETRIES=3
```

4. **Iniciar el servidor**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

5. **Abrir en el navegador**
```
http://localhost:8000
```

## 📖 Uso

### Interfaz Web

1. Ingresa palabras clave en el campo de búsqueda
2. Ajusta los filtros según tus necesidades
3. Haz clic en "Buscar"
4. Exporta los resultados a CSV o accede a los DOIs

### API REST

#### Buscar referencias

```bash
curl "http://localhost:8000/search?q=machine+learning&rows=10"
```

#### Exportar a CSV

```bash
curl "http://localhost:8000/export/csv?q=climate+change&max_results=100" -o results.csv
```

#### Exportar a BibTeX

```bash
curl "http://localhost:8000/export/bibtex?dois=10.1038/s41586-019-1666-5" -o paper.bib
```

Ver la [documentación completa](http://localhost:8000/static/docs.html) para más ejemplos.

## 🏗️ Arquitectura

```
uiresearch/
├── app/
│   ├── main.py              # Aplicación FastAPI
│   ├── config.py            # Configuración
│   ├── models.py            # Modelos de datos
│   ├── services/            # Servicios de negocio
│   │   ├── crossref_client.py
│   │   ├── search_service.py
│   │   └── export_service.py
│   ├── utils/               # Utilidades
│   │   ├── normalizer.py
│   │   ├── validators.py
│   │   └── logger.py
│   └── static/              # Frontend
│       ├── index.html
│       ├── docs.html
│       ├── app.js
│       └── styles.css
├── tests/                   # Tests (próximamente)
├── requirements.txt
└── README.md
```

## 🛠️ Tecnologías

- **Backend**: FastAPI, Python 3.10+
- **HTTP Client**: httpx (async)
- **Validación**: Pydantic
- **Logging**: structlog
- **Métricas**: Prometheus
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Fuentes**: Inter (Google Fonts)

## 📊 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Interfaz web principal |
| `/search` | GET | Buscar referencias académicas |
| `/export/csv` | GET | Exportar resultados a CSV |
| `/export/bibtex` | GET | Exportar referencias a BibTeX |
| `/healthz` | GET | Health check |
| `/metrics` | GET | Métricas Prometheus |
| `/docs` | GET | Documentación OpenAPI |

## 🔧 Configuración

### Variables de entorno

| Variable | Descripción | Por defecto |
|----------|-------------|-------------|
| `APP_USER_AGENT` | Identificador de la aplicación | UIResearch/1.0 |
| `APP_MAILTO` | Email de contacto (requerido) | - |
| `PORT` | Puerto del servidor | 8000 |
| `LOG_LEVEL` | Nivel de logging | INFO |
| `CROSSREF_TIMEOUT` | Timeout para peticiones (segundos) | 30 |
| `MAX_RETRIES` | Número máximo de reintentos | 3 |

## 🐳 Docker (próximamente)

```bash
docker build -t uiresearch .
docker run -p 8000:8000 --env-file .env uiresearch
```

## 🧪 Tests (próximamente)

```bash
pytest tests/
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Diego Bustos**

- LinkedIn: [@inginddie](https://www.linkedin.com/in/inginddie)
- GitHub: [@inginddie](https://github.com/inginddie)

## 🙏 Agradecimientos

- [Crossref](https://www.crossref.org/) por proporcionar la API pública
- Comunidad de FastAPI por el excelente framework
- Todos los contribuidores y usuarios de UIResearch

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📮 Soporte

Si tienes problemas o preguntas:

1. Revisa la [documentación](http://localhost:8000/static/docs.html)
2. Busca en los [issues existentes](https://github.com/inginddie/uiresearch/issues)
3. Crea un [nuevo issue](https://github.com/inginddie/uiresearch/issues/new)

---

<div align="center">

**⭐ Si te gusta este proyecto, dale una estrella en GitHub! ⭐**

Hecho con ❤️ por [Diego Bustos](https://www.linkedin.com/in/inginddie)

</div>
