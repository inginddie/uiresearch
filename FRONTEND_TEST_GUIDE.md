# 🎨 Guía de Prueba del Frontend de Autenticación

## 📋 CHECKLIST DE PRUEBAS

### ✅ ANTES DE EMPEZAR

**Requisitos:**
1. PostgreSQL configurado en Railway
2. Variables de entorno configuradas:
   - `DATABASE_URL`
   - `JWT_SECRET_KEY`
   - `JWT_ALGORITHM`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`
3. Tablas creadas en la base de datos
4. Deploy exitoso en Railway

---

## 🧪 PRUEBAS A REALIZAR

### 1. Página de Registro (Signup)

**URL**: `https://tu-url.railway.app/static/signup.html`

**Pruebas:**

✅ **Diseño Visual**
- [ ] La página se ve bien en desktop
- [ ] La página se ve bien en mobile
- [ ] Los colores coinciden con el diseño principal
- [ ] El logo y navbar se muestran correctamente

✅ **Validación de Formulario**
- [ ] Email inválido muestra error
- [ ] Contraseña < 8 caracteres muestra error
- [ ] Contraseñas no coinciden muestra error
- [ ] Términos no aceptados muestra error

✅ **Registro Exitoso**
1. Completa el formulario:
   - Nombre: `Test User`
   - Email: `test@example.com`
   - Contraseña: `testpassword123`
   - Confirmar contraseña: `testpassword123`
   - ✓ Acepto términos
2. Click "Crear Cuenta"
3. Debe mostrar: "¡Cuenta creada exitosamente!"
4. Debe redirigir a `/static/login.html` en 2 segundos

✅ **Registro Duplicado**
1. Intenta registrar el mismo email otra vez
2. Debe mostrar: "Email already registered"

---

### 2. Página de Login

**URL**: `https://tu-url.railway.app/static/login.html`

**Pruebas:**

✅ **Diseño Visual**
- [ ] La página se ve bien en desktop
- [ ] La página se ve bien en mobile
- [ ] Botón de "Recordarme" funciona
- [ ] Link a "¿Olvidaste tu contraseña?" visible

✅ **Login Exitoso**
1. Ingresa credenciales:
   - Email: `test@example.com`
   - Contraseña: `testpassword123`
2. Click "Iniciar Sesión"
3. Debe mostrar: "¡Inicio de sesión exitoso!"
4. Debe redirigir a `/` en 1 segundo

✅ **Login Fallido**
1. Ingresa contraseña incorrecta
2. Debe mostrar: "Incorrect email or password"
3. No debe redirigir

---

### 3. Navbar con Autenticación

**URL**: `https://tu-url.railway.app/`

**Pruebas:**

✅ **Usuario NO Autenticado**
- [ ] Se muestran botones "Iniciar Sesión" y "Registrarse"
- [ ] NO se muestra el email del usuario
- [ ] NO se muestra botón "Cerrar Sesión"

✅ **Usuario Autenticado**
1. Inicia sesión primero
2. Ve a la página principal
3. Debe mostrar:
   - [ ] Email del usuario en el navbar
   - [ ] Botón "Cerrar Sesión"
   - [ ] NO se muestran botones de login/signup

✅ **Cerrar Sesión**
1. Click en "Cerrar Sesión"
2. Debe mostrar: "Sesión cerrada exitosamente"
3. Debe volver a mostrar botones de login/signup
4. El email del usuario debe desaparecer

---

### 4. Persistencia de Sesión

**Pruebas:**

✅ **Token Guardado**
1. Inicia sesión
2. Abre DevTools → Application → Local Storage
3. Debe existir `auth_token` con un valor JWT

✅ **Sesión Persiste**
1. Inicia sesión
2. Cierra la pestaña
3. Abre la página de nuevo
4. Debe seguir mostrando el usuario autenticado

✅ **Auto-redirect si ya está logueado**
1. Inicia sesión
2. Intenta ir a `/static/login.html`
3. Debe redirigir automáticamente a `/`

---

### 5. Manejo de Errores

**Pruebas:**

✅ **Sin Conexión a Internet**
1. Desconecta internet
2. Intenta hacer login
3. Debe mostrar: "Error de conexión"

✅ **Backend Caído**
1. Si el backend no responde
2. Debe mostrar error apropiado
3. No debe romper la página

✅ **Token Expirado**
1. Espera 30 minutos (o modifica el token)
2. Recarga la página
3. Debe cerrar sesión automáticamente

---

## 🎯 PRUEBAS VISUALES

### Desktop (1920x1080)
- [ ] Formularios centrados
- [ ] Sidebar de beneficios visible
- [ ] Espaciado correcto
- [ ] Botones del tamaño adecuado

### Tablet (768x1024)
- [ ] Layout de 1 columna
- [ ] Formularios ocupan todo el ancho
- [ ] Sidebar debajo del formulario
- [ ] Todo legible

### Mobile (375x667)
- [ ] Formularios responsive
- [ ] Botones fáciles de tocar
- [ ] Texto legible
- [ ] No hay scroll horizontal

---

## 🐛 PROBLEMAS COMUNES

### Error: "Cannot import name 'SearchFilters'"
**Solución**: Ya resuelto en commit anterior

### Error: "DATABASE_URL environment variable is required"
**Solución**: Configurar PostgreSQL en Railway

### Error: "relation 'users' does not exist"
**Solución**: Ejecutar `database/schema.sql` en Railway

### Login no funciona
**Verificar**:
1. PostgreSQL está corriendo
2. Variables de entorno configuradas
3. Tablas creadas
4. Backend responde en `/healthz`

### Token no se guarda
**Verificar**:
1. Abrir DevTools → Console
2. Buscar errores de JavaScript
3. Verificar que localStorage esté habilitado

---

## 📊 MÉTRICAS DE ÉXITO

### ✅ TODO FUNCIONA SI:

1. **Registro**
   - ✅ Puedes crear una cuenta nueva
   - ✅ Recibes mensaje de éxito
   - ✅ Redirige a login

2. **Login**
   - ✅ Puedes iniciar sesión
   - ✅ Token se guarda en localStorage
   - ✅ Redirige a home

3. **Navbar**
   - ✅ Muestra email cuando estás logueado
   - ✅ Muestra botones cuando NO estás logueado
   - ✅ Logout funciona correctamente

4. **Persistencia**
   - ✅ Sesión persiste al recargar
   - ✅ Auto-redirect funciona
   - ✅ Token expira correctamente

---

## 🎨 CAPTURAS DE PANTALLA

### Signup Page
```
┌─────────────────────────────────────────┐
│  UIResearch                    Docs     │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────┐  ┌──────────────┐  │
│  │ Crear Cuenta  │  │ Plan Gratuito│  │
│  │               │  │ incluye:     │  │
│  │ [Nombre]      │  │ • 10 búsq/día│  │
│  │ [Email]       │  │ • 50 result. │  │
│  │ [Password]    │  │ • CSV export │  │
│  │ [Confirm]     │  │ • Sin tarjeta│  │
│  │ ☑ Términos    │  └──────────────┘  │
│  │ [Crear Cuenta]│                     │
│  └───────────────┘                     │
└─────────────────────────────────────────┘
```

### Login Page
```
┌─────────────────────────────────────────┐
│  UIResearch                    Docs     │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────┐  ┌──────────────┐  │
│  │ Iniciar Sesión│  │ ¿Por qué     │  │
│  │               │  │ crear cuenta?│  │
│  │ [Email]       │  │ • Ilimitadas │  │
│  │ [Password]    │  │ • Historial  │  │
│  │ ☐ Recordarme  │  │ • CSV/BibTeX │  │
│  │ [Iniciar]     │  │ • API access │  │
│  └───────────────┘  └──────────────┘  │
└─────────────────────────────────────────┘
```

### Navbar (Logged In)
```
┌─────────────────────────────────────────┐
│ 🔍 UIResearch  Búsqueda  Docs           │
│                    test@example.com     │
│                    [Cerrar Sesión]      │
└─────────────────────────────────────────┘
```

---

## 🚀 SIGUIENTE PASO

Una vez que todas las pruebas pasen:

1. **Configurar Stripe** (Día 4-5 del plan)
2. **Crear página de pricing** (Semana 2)
3. **Implementar rate limiting** (Semana 3)
4. **Agregar features premium** (Semana 3)

---

## 📞 SOPORTE

Si algo no funciona:
1. Revisa los logs en Railway Dashboard
2. Abre DevTools → Console para ver errores
3. Verifica que PostgreSQL esté corriendo
4. Prueba los endpoints con `test_auth.py`

---

**¡Listo para probar!** 🎉

Abre tu app en Railway y prueba el flujo completo de registro → login → logout.
