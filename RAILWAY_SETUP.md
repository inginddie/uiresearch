# 🚂 Railway PostgreSQL Setup - Guía Visual

## 📋 CHECKLIST RÁPIDO

- [ ] Crear servicio PostgreSQL en Railway
- [ ] Copiar DATABASE_URL
- [ ] Agregar variables de entorno
- [ ] Ejecutar schema SQL
- [ ] Verificar tablas creadas
- [ ] Probar endpoints

---

## 🎯 PASO 1: Crear PostgreSQL en Railway

### 1.1 Ir a tu proyecto

1. Ve a: https://railway.app/dashboard
2. Click en tu proyecto **"uiresearch"** (o como lo hayas nombrado)
3. Deberías ver tu servicio web actual

### 1.2 Agregar PostgreSQL

1. Click en el botón **"+ New"** (esquina superior derecha)
2. Selecciona **"Database"**
3. Click en **"Add PostgreSQL"**
4. Espera 1-2 minutos mientras se crea

✅ **Resultado**: Verás un nuevo servicio llamado "Postgres" en tu proyecto

---

## 🔑 PASO 2: Obtener DATABASE_URL

### 2.1 Acceder al servicio PostgreSQL

1. Click en el servicio **"Postgres"** que acabas de crear
2. Ve a la pestaña **"Variables"**
3. Busca la variable **"DATABASE_URL"**

### 2.2 Copiar la URL

La URL se verá así:
```
postgresql://postgres:CONTRASEÑA@SERVIDOR.railway.app:5432/railway
```

**IMPORTANTE**: Copia esta URL completa, la necesitarás en el siguiente paso.

---

## ⚙️ PASO 3: Configurar Variables de Entorno

### 3.1 Ir a tu servicio web

1. Click en tu servicio **web** (no el Postgres)
2. Ve a la pestaña **"Variables"**

### 3.2 Agregar variables necesarias

Click en **"+ New Variable"** y agrega cada una:

#### Variable 1: DATABASE_URL
```
DATABASE_URL = postgresql://postgres:CONTRASEÑA@SERVIDOR.railway.app:5432/railway
```
(Pega la URL que copiaste del paso anterior)

#### Variable 2: JWT_SECRET_KEY
```
JWT_SECRET_KEY = [GENERA UNA CLAVE ALEATORIA]
```

**Para generar una clave segura**, ejecuta en tu terminal:

```bash
# Windows PowerShell
python -c "import secrets; print(secrets.token_urlsafe(32))"

# O usa este valor temporal (CÁMBIALO EN PRODUCCIÓN):
JWT_SECRET_KEY = dev-secret-key-change-in-production-12345678
```

#### Variable 3: JWT_ALGORITHM
```
JWT_ALGORITHM = HS256
```

#### Variable 4: ACCESS_TOKEN_EXPIRE_MINUTES
```
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### 3.3 Verificar variables

Deberías tener estas variables en tu servicio web:
- ✅ DATABASE_URL
- ✅ JWT_SECRET_KEY
- ✅ JWT_ALGORITHM
- ✅ ACCESS_TOKEN_EXPIRE_MINUTES
- ✅ APP_USER_AGENT (ya existente)
- ✅ APP_MAILTO (ya existente)
- ✅ CORS_ORIGINS (ya existente)

---

## 🗄️ PASO 4: Crear Tablas en la Base de Datos

### 4.1 Abrir Query Editor

1. Click en el servicio **"Postgres"**
2. Ve a la pestaña **"Data"**
3. Click en **"Query"** (botón en la parte superior)

### 4.2 Ejecutar el Schema SQL

1. Abre el archivo `database/schema.sql` en tu editor
2. **Copia TODO el contenido** (Ctrl+A, Ctrl+C)
3. **Pega** en el Query Editor de Railway
4. Click en **"Run Query"** o presiona Ctrl+Enter

### 4.3 Verificar que se crearon las tablas

1. Ve a la pestaña **"Tables"** (al lado de "Query")
2. Deberías ver estas tablas:
   - ✅ users
   - ✅ subscriptions
   - ✅ usage_tracking
   - ✅ search_history
   - ✅ favorites

**Si ves las 5 tablas, ¡perfecto!** 🎉

---

## 🚀 PASO 5: Deploy y Verificación

### 5.1 Railway hará auto-deploy

Railway detectará las nuevas variables y hará redeploy automáticamente.

**Espera 2-3 minutos** mientras se despliega.

### 5.2 Verificar que el deploy fue exitoso

1. Ve a la pestaña **"Deployments"** de tu servicio web
2. El último deployment debe estar en estado **"Success"** (verde)
3. Si hay errores, revisa los **"Logs"**

### 5.3 Obtener tu URL de producción

1. Ve a la pestaña **"Settings"** de tu servicio web
2. Busca **"Domains"**
3. Copia tu URL (ejemplo: `https://web-production-f69ce.up.railway.app`)

---

## ✅ PASO 6: Probar los Endpoints

### 6.1 Healthcheck

```bash
curl https://TU-URL.railway.app/healthz
```

Respuesta esperada:
```json
{"status":"ok"}
```

### 6.2 Registrar un usuario

```bash
curl -X POST https://TU-URL.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
  }'
```

Respuesta esperada:
```json
{
  "id": 1,
  "email": "test@example.com",
  "full_name": "Test User",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-10-18T..."
}
```

### 6.3 Login

```bash
curl -X POST https://TU-URL.railway.app/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword123"
```

Respuesta esperada:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 6.4 Obtener usuario actual

```bash
# Reemplaza YOUR_TOKEN con el token del paso anterior
curl https://TU-URL.railway.app/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Respuesta esperada:
```json
{
  "id": 1,
  "email": "test@example.com",
  "full_name": "Test User",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-10-18T..."
}
```

---

## 🎉 ¡LISTO!

Si todos los pasos funcionaron, tu sistema de autenticación está **100% operativo** en producción.

---

## 🐛 Troubleshooting

### Error: "DATABASE_URL environment variable is required"

**Causa**: La variable DATABASE_URL no está configurada.

**Solución**:
1. Ve a Variables en tu servicio web
2. Verifica que DATABASE_URL esté presente
3. Si no está, agrégala con la URL del servicio Postgres

### Error: "relation 'users' does not exist"

**Causa**: Las tablas no se crearon en la base de datos.

**Solución**:
1. Ve al servicio Postgres → Data → Query
2. Ejecuta el contenido de `database/schema.sql`
3. Verifica en la pestaña Tables

### Error: "password authentication failed"

**Causa**: La DATABASE_URL es incorrecta.

**Solución**:
1. Ve al servicio Postgres → Variables
2. Copia la DATABASE_URL exacta
3. Actualiza la variable en tu servicio web

### Error: "Could not validate credentials"

**Causa**: El token JWT expiró o es inválido.

**Solución**:
1. Haz login nuevamente para obtener un nuevo token
2. Los tokens expiran en 30 minutos por defecto

### El deploy falla con errores de importación

**Causa**: Dependencias no instaladas correctamente.

**Solución**:
1. Verifica que `requirements.txt` esté actualizado
2. Railway reinstalará las dependencias automáticamente
3. Revisa los logs de build

---

## 📊 Verificar Datos en la Base de Datos

### Ver usuarios registrados

1. Ve a Postgres → Data → Query
2. Ejecuta:

```sql
SELECT id, email, full_name, is_active, is_verified, created_at 
FROM users
ORDER BY created_at DESC;
```

### Ver todas las tablas

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

### Contar usuarios

```sql
SELECT COUNT(*) as total_users FROM users;
```

---

## 🔐 Seguridad en Producción

### ⚠️ IMPORTANTE - Antes de lanzar públicamente:

- [ ] Cambiar JWT_SECRET_KEY a un valor aleatorio seguro
- [ ] Verificar que CORS_ORIGINS solo incluya tu dominio
- [ ] Habilitar HTTPS (Railway lo hace automáticamente)
- [ ] Configurar rate limiting apropiado
- [ ] Revisar logs regularmente
- [ ] Hacer backup de la base de datos

---

## 📞 Siguiente Paso

Una vez que todo funcione:

**Opción A**: Configurar Stripe (Día 4-5 del plan)
**Opción B**: Crear frontend de login/signup (Semana 2)
**Opción C**: Implementar rate limiting por usuario (Semana 3)

---

**¿Necesitas ayuda con algún paso?** Avísame y te guío. 🚀
