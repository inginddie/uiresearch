# UIResearch - Roadmap de Monetización

## 🎯 Objetivo
Convertir UIResearch en un producto SaaS rentable para investigadores y académicos.

---

## 📊 FASE 1: VALIDACIÓN (Semanas 1-2)

### ✅ Tareas Inmediatas

#### 1. Instalar Google Analytics
- [ ] Crear cuenta en Google Analytics
- [ ] Agregar tracking code a index.html y docs.html
- [ ] Configurar eventos personalizados:
  - Búsquedas realizadas
  - Exportaciones CSV
  - Exportaciones BibTeX
  - Tiempo en sitio
  - Páginas visitadas

#### 2. Agregar formulario de feedback
- [ ] Crear modal de feedback en la UI
- [ ] Preguntas clave:
  - ¿Qué feature te gustaría ver?
  - ¿Pagarías por esta herramienta?
  - ¿Cuánto estarías dispuesto a pagar?
  - ¿Qué te falta?

#### 3. Promoción inicial
- [ ] Publicar en Product Hunt
- [ ] Compartir en Reddit:
  - r/academia
  - r/GradSchool
  - r/AskAcademia
  - r/PhD
  - r/research
- [ ] Compartir en Twitter con hashtags:
  - #AcademicTwitter
  - #PhDLife
  - #Research
  - #OpenScience
- [ ] Contactar a 10 influencers académicos en LinkedIn
- [ ] Publicar en grupos de Facebook de investigadores

#### 4. Recoger feedback
- [ ] Entrevistar a 10-20 usuarios
- [ ] Identificar pain points
- [ ] Validar willingness to pay
- [ ] Priorizar features

**Meta**: 100-500 usuarios activos mensuales

---

## 💎 FASE 2: MODELO FREEMIUM (Semanas 3-4)

### Plan de Precios

```
🆓 FREE TIER
├─ 10 búsquedas/día
├─ 50 resultados máximo por búsqueda
├─ Exportación CSV básica
├─ Ads discretos (opcional)
└─ Marca de agua "Powered by UIResearch"

💼 PRO - $9.99/mes o $99/año (ahorra 17%)
├─ Búsquedas ilimitadas
├─ 500 resultados máximo
├─ Exportación CSV + BibTeX
├─ Sin ads
├─ Historial de búsquedas (últimos 30 días)
├─ Guardado de favoritos
├─ Alertas por email (nuevos papers)
└─ Soporte prioritario

🏢 TEAM - $29.99/mes o $299/año
├─ Todo de PRO
├─ 5 usuarios
├─ 1000 resultados máximo
├─ API access (1000 calls/mes)
├─ Workspace compartido
├─ Exportación masiva
├─ Integraciones (Zotero, Mendeley)
└─ Soporte dedicado

🎓 ACADEMIC - $4.99/mes (50% descuento)
├─ Todo de PRO
├─ Precio especial para estudiantes
└─ Verificación con email .edu
```

### Implementación Técnica

#### 2.1 Sistema de Autenticación
- [ ] Integrar Auth0 o Supabase Auth
- [ ] Crear páginas:
  - /login
  - /signup
  - /dashboard
  - /settings
- [ ] Implementar JWT tokens
- [ ] Middleware de autenticación

#### 2.2 Base de Datos
- [ ] Configurar PostgreSQL en Railway
- [ ] Tablas necesarias:
  - users (id, email, plan, created_at)
  - subscriptions (id, user_id, plan, status, stripe_id)
  - searches (id, user_id, query, results_count, created_at)
  - favorites (id, user_id, doi, created_at)

#### 2.3 Pasarela de Pagos
- [ ] Crear cuenta en Stripe
- [ ] Configurar productos y precios
- [ ] Implementar Stripe Checkout
- [ ] Webhooks para:
  - subscription.created
  - subscription.updated
  - subscription.deleted
  - payment.succeeded
  - payment.failed

#### 2.4 Rate Limiting por Tier
- [ ] Free: 10 búsquedas/día
- [ ] Pro: ilimitado
- [ ] Team: ilimitado + API
- [ ] Tracking de uso por usuario

#### 2.5 Dashboard de Usuario
- [ ] Historial de búsquedas
- [ ] Búsquedas guardadas
- [ ] Estadísticas de uso
- [ ] Gestión de suscripción
- [ ] Facturación

---

## 🚀 FASE 3: FEATURES PREMIUM (Semanas 5-8)

### 3.1 Búsqueda Avanzada
- [ ] Búsqueda por autor específico
- [ ] Búsqueda por institución
- [ ] Búsqueda por journal específico
- [ ] Filtros por número de citas
- [ ] Filtros por open access
- [ ] Búsqueda booleana (AND, OR, NOT)

### 3.2 Análisis y Visualización
- [ ] Gráficos de tendencias por año
- [ ] Nube de palabras clave
- [ ] Red de co-autores
- [ ] Análisis de impacto
- [ ] Comparación de journals
- [ ] Métricas de citación

### 3.3 Integraciones
- [ ] Zotero integration
- [ ] Mendeley integration
- [ ] Google Scholar alerts
- [ ] Notion integration
- [ ] Obsidian plugin
- [ ] Slack notifications

### 3.4 Colaboración
- [ ] Workspaces compartidos
- [ ] Comentarios en papers
- [ ] Listas colaborativas
- [ ] Compartir búsquedas
- [ ] Permisos por usuario

### 3.5 API para Desarrolladores
- [ ] API key management
- [ ] Webhooks
- [ ] Rate limits personalizados
- [ ] Documentación extendida
- [ ] SDKs (Python, JavaScript)

### 3.6 Alertas y Notificaciones
- [ ] Alertas por email para nuevos papers
- [ ] Notificaciones push
- [ ] Resumen semanal
- [ ] Alertas por autor
- [ ] Alertas por keywords

---

## 📈 FASE 4: ESCALAMIENTO (Meses 3-6)

### 4.1 Marketing de Contenido
- [ ] Blog con tutoriales académicos
- [ ] Guías de investigación
- [ ] Casos de estudio
- [ ] SEO optimizado
- [ ] Newsletter semanal
- [ ] Webinars mensuales

### 4.2 Partnerships
- [ ] Universidades (licencias institucionales)
- [ ] Bibliotecas académicas
- [ ] Plataformas de e-learning
- [ ] Journals científicos
- [ ] Asociaciones de investigadores

### 4.3 Programa de Afiliados
- [ ] 20% comisión recurrente
- [ ] Dashboard de afiliados
- [ ] Material de marketing
- [ ] Tracking de conversiones

### 4.4 Licencias Institucionales
```
🏛️ INSTITUTIONAL - $499/año
├─ 50 usuarios
├─ Todo ilimitado
├─ SSO integration (SAML)
├─ Custom branding
├─ Dedicated support
├─ SLA garantizado
├─ Training sessions
└─ Custom reports
```

### 4.5 Expansión de Features
- [ ] Integración con más APIs (Scopus, PubMed)
- [ ] Machine Learning para recomendaciones
- [ ] Traducción automática de abstracts
- [ ] Análisis de sentimiento
- [ ] Detección de plagio
- [ ] Generación de resúmenes con AI

---

## 💰 PROYECCIÓN FINANCIERA

### Año 1 (Conservadora)

**Mes 1-2**: $0 (validación)
**Mes 3**: $100-500 (primeros pagos)
**Mes 4**: $500-1,500
**Mes 5**: $1,500-3,000
**Mes 6**: $3,000-5,000
**Mes 7-12**: Crecimiento 20% mensual

**Total Año 1**: $15,000-30,000 MRR

### Asumiendo:
- 1,000 usuarios free
- 50 usuarios Pro ($9.99) = $500/mes
- 5 usuarios Team ($29.99) = $150/mes
- 2 licencias institucionales ($499) = $1,000/mes
- **Total**: ~$1,650/mes inicial

### Año 2 (Optimista)

- 10,000 usuarios free
- 500 usuarios Pro = $5,000/mes
- 50 usuarios Team = $1,500/mes
- 20 licencias institucionales = $10,000/mes
- **Total**: ~$16,500/mes = $198,000/año

---

## 📊 MÉTRICAS CLAVE

### Product Metrics
- DAU/MAU (usuarios activos)
- Búsquedas por usuario
- Tasa de conversión free → pro
- Churn rate
- LTV (lifetime value)
- Engagement rate

### Business Metrics
- MRR (monthly recurring revenue)
- ARR (annual recurring revenue)
- CAC (customer acquisition cost)
- Payback period
- Gross margin
- Net revenue retention

---

## 🛠️ STACK TÉCNICO ADICIONAL

### Backend
- PostgreSQL (usuarios, suscripciones)
- Redis (cache, rate limiting, sessions)
- Celery (tareas asíncronas)
- RabbitMQ o Redis (message queue)

### Autenticación
- Auth0 / Supabase / Firebase Auth

### Pagos
- Stripe (principal)
- PayPal (alternativa)

### Email
- SendGrid / Mailgun (transaccional)
- ConvertKit / Mailchimp (marketing)

### Analytics
- Mixpanel / Amplitude (product analytics)
- Google Analytics (web analytics)
- Hotjar (heatmaps, recordings)

### Monitoring
- Sentry (error tracking)
- Prometheus + Grafana (ya tienes)
- Uptime Robot (monitoring)

### Hosting
- Railway (backend) ✅
- Vercel (frontend estático - opcional)
- Cloudflare (CDN)

---

## ✅ CHECKLIST SEMANAL

### Semana 1
- [ ] Instalar Google Analytics
- [ ] Agregar formulario de feedback
- [ ] Publicar en Product Hunt
- [ ] Compartir en 5 subreddits
- [ ] Contactar 10 influencers

### Semana 2
- [ ] Analizar primeros datos
- [ ] Entrevistar 10 usuarios
- [ ] Definir pricing final
- [ ] Diseñar página de pricing
- [ ] Crear mockups de dashboard

### Semana 3
- [ ] Implementar Auth0
- [ ] Configurar PostgreSQL
- [ ] Crear tablas de BD
- [ ] Implementar login/signup
- [ ] Crear dashboard básico

### Semana 4
- [ ] Integrar Stripe
- [ ] Implementar checkout
- [ ] Configurar webhooks
- [ ] Testing de pagos
- [ ] Lanzar versión Pro

---

## 🚨 RIESGOS Y MITIGACIONES

### Riesgo 1: Baja adopción
**Mitigación**: 
- Marketing agresivo inicial
- Tier gratuito generoso
- Recoger feedback constantemente

### Riesgo 2: Competencia
**Mitigación**:
- Diferenciación por UX
- Features únicas (colaboración, AI)
- Precio competitivo

### Riesgo 3: Costos de infraestructura
**Mitigación**:
- Optimizar queries
- Implementar cache agresivo
- Escalar gradualmente

### Riesgo 4: Churn alto
**Mitigación**:
- Onboarding excelente
- Soporte rápido
- Features que generen hábito
- Alertas y notificaciones

---

## 🎯 DEFINITION OF SUCCESS

### Mes 3
- ✅ 500 usuarios registrados
- ✅ 10 clientes de pago
- ✅ $100 MRR

### Mes 6
- ✅ 2,000 usuarios registrados
- ✅ 50 clientes de pago
- ✅ $1,000 MRR

### Año 1
- ✅ 10,000 usuarios registrados
- ✅ 200 clientes de pago
- ✅ $5,000 MRR
- ✅ 5 licencias institucionales

---

## 📚 RECURSOS RECOMENDADOS

### Libros
- "The Mom Test" - Rob Fitzpatrick
- "Traction" - Gabriel Weinberg
- "Zero to Sold" - Arvid Kahl
- "The SaaS Playbook" - Rob Walling

### Comunidades
- Indie Hackers
- MicroConf
- SaaS subreddit
- Hacker News

### Herramientas
- Stripe Atlas (crear empresa)
- Gumroad (alternativa simple)
- Lemon Squeezy (merchant of record)
- Paddle (pagos globales)

---

## 💬 PRÓXIMOS PASOS INMEDIATOS

1. **Esta semana**: Instalar Analytics + Feedback
2. **Próxima semana**: Promoción + Entrevistas
3. **Semana 3**: Implementar Auth
4. **Semana 4**: Integrar Stripe y lanzar Pro

---

**Última actualización**: Octubre 2025
**Versión**: 1.0
**Autor**: Diego Bustos
