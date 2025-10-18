# 🚀 Setup Guide - Sistema de Autenticación

## ✅ PASO 1: Instalar Dependencias

```bash
pip install -r requirements.txt
```

## ✅ PASO 2: Configurar PostgreSQL en Railway

### 2.1 Crear Base de Datos

1. Ve a tu proyecto en Railway: https://railway.app
2. Click en **"New"** → **"Database"** → **"Add PostgreSQL"**
3. Espera a que se cree (1-2 minutos)

### 2.2 Obtener DATABASE_URL

1. Click en el servicio PostgreSQL
2. Ve a la pestaña **"Variables"**
3. Copia el valor de `DATABASE_URL`
4. Debería verse así: `postgresql://postgres:password@host:5432/railway`

### 2.3 Agregar a Variables de Entorno

**En Railway (para producción)**:
1. Ve a tu servicio web (no el PostgreSQL)
2. Click en **"Variables"**
3. Click **"New Variable"**
4. Agrega:
   - `DATABASE_URL` = (pega la URL que copiaste)
   - `JWT_SECRET_KEY` = (genera una clave aleatoria segura)

**Localmente (para desarrollo)**:
1. Copia `.env.example` a `.env`
2. Actualiza `DATABASE_URL` con la URL de Railway
3. Genera un `JWT_SECRET_KEY` seguro

```bash
# Generar JWT_SECRET_KEY (Python)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## ✅ PASO 3: Crear Tablas en la Base de Datos

### Opción A: Usando Railway Dashboard (Recomendado)

1. En Railway, click en tu servicio PostgreSQL
2. Ve a la pestaña **"Data"**
3. Click en **"Query"**
4. Copia y pega el contenido de `database/schema.sql`
5. Click **"Run Query"**
6. Verifica que las tablas se crearon en la pestaña **"Tables"**

### Opción B: Usando psql (Avanzado)

```bash
# Conectar a la base de datos
psql "postgresql://postgres:password@host:5432/railway"

# Ejecutar el script
\i database/schema.sql

# Verificar tablas
\dt

# Salir
\q
```

## ✅ PASO 4: Verificar Instalación

### 4.1 Iniciar el servidor localmente

```bash
uvicorn app.main:app --reload
```

### 4.2 Probar endpoints de auth

**Healthcheck**:
```bash
curl http://localhost:8000/healthz
```

**Registro de usuario**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
  }'
```

**Login**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword123"
```

Deberías recibir un token JWT:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

**Obtener usuario actual**:
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## ✅ PASO 5: Deploy a Railway

### 5.1 Commit y Push

```bash
git add .
git commit -m "Add authentication system"
git push origin main
```

### 5.2 Railway Auto-Deploy

Railway detectará los cambios y hará deploy automáticamente.

### 5.3 Verificar en Producción

```bash
# Reemplaza con tu URL de Railway
curl https://web-production-f69ce.up.railway.app/healthz
```

## 🎯 PRÓXIMOS PASOS

Una vez que el auth funcione:

1. **Crear frontend de login/signup** (Semana 2)
2. **Integrar Stripe** (Semana 1, Día 4-5)
3. **Implementar rate limiting por usuario** (Semana 3)
4. **Agregar features premium** (Semana 3)

## 🐛 Troubleshooting

### Error: "DATABASE_URL environment variable is required"

**Solución**: Asegúrate de que `DATABASE_URL` esté configurada en Railway Variables.

### Error: "relation 'users' does not exist"

**Solución**: Ejecuta el script `database/schema.sql` en PostgreSQL.

### Error: "password authentication failed"

**Solución**: Verifica que la `DATABASE_URL` sea correcta y que el servicio PostgreSQL esté activo.

### Error: "Could not validate credentials"

**Solución**: Verifica que el token JWT sea válido y no haya expirado (30 minutos por defecto).

## 📊 Verificar Base de Datos

### Ver usuarios registrados

```sql
SELECT id, email, full_name, is_active, is_verified, created_at 
FROM users;
```

### Ver suscripciones

```sql
SELECT u.email, s.plan, s.status, s.created_at
FROM subscriptions s
JOIN users u ON s.user_id = u.id;
```

## 🔒 Seguridad

### Producción Checklist

- [ ] Cambiar `JWT_SECRET_KEY` a un valor aleatorio seguro
- [ ] Usar HTTPS en producción (Railway lo hace automáticamente)
- [ ] Configurar CORS correctamente
- [ ] Habilitar rate limiting
- [ ] Revisar logs regularmente

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Railway Dashboard
2. Verifica que todas las variables de entorno estén configuradas
3. Prueba localmente primero antes de hacer deploy

---

**¡Listo! Tu sistema de autenticación está funcionando.** 🎉
