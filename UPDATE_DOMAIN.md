# Actualizar dominio en el proyecto

Una vez que tu dominio esté activo, actualiza estos archivos:

## 1. README.md

Reemplaza:
```
https://web-production-f69ce.up.railway.app
```

Con:
```
https://uiresearch.app
```

## 2. app/static/index.html

Actualiza meta tags (si los agregas):
```html
<meta property="og:url" content="https://uiresearch.app">
<link rel="canonical" href="https://uiresearch.app">
```

## 3. app/static/docs.html

Actualiza links internos si es necesario.

## 4. Variables de entorno en Railway

```
CORS_ORIGINS=https://uiresearch.app,https://www.uiresearch.app
```

## 5. Publicaciones

- LinkedIn: Edita el post con la nueva URL
- YouTube: Actualiza la descripción
- GitHub: README ya estará actualizado

## Comandos Git

```bash
git add .
git commit -m "🌐 Update to custom domain"
git push origin main
```
