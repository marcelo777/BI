# 🚀 Guía de Deployment - Dashboard Enterprise

## Opciones para Publicar tu Dashboard KPI

### 🌟 OPCIÓN 1: Streamlit Community Cloud (RECOMENDADO - GRATIS)

#### ✅ Ventajas
- **Completamente gratuito**
- **Fácil de configurar** (5 minutos)
- **Dominio público** automático
- **Integración directa con GitHub**
- **SSL incluido** (https://)
- **Actualizaciones automáticas**

#### 📋 Pasos para Deployment

1. **Subir a GitHub**
```bash
# Crear repositorio en GitHub (desde GitHub.com)
# Clonar el repositorio localmente
git clone https://github.com/TU_USUARIO/kpi-dashboard-enterprise.git
cd kpi-dashboard-enterprise

# Copiar archivos del proyecto
cp -r C:/Users/marce/Downloads/BI/proyecto_kpi_dashboard/* .

# Subir archivos
git add .
git commit -m "Dashboard Enterprise KPI - Initial deployment"
git push origin main
```

2. **Configurar Streamlit Cloud**
- Ir a: https://share.streamlit.io/
- **Sign in** con tu cuenta de GitHub
- Click en **"New app"**
- Seleccionar tu repositorio: `kpi-dashboard-enterprise`
- Main file path: `dashboard_enterprise.py`
- Click **"Deploy!"**

3. **URL Pública**
Tu dashboard estará disponible en:
```
https://TU_USUARIO-kpi-dashboard-enterprise-dashboard-enterprise-HASH.streamlit.app/
```

#### 🔧 Archivos Necesarios para Streamlit Cloud

**requirements.txt** (ya lo tienes):
```txt
streamlit>=1.49.1
plotly>=6.3.0
pandas>=2.3.2
numpy>=2.3.3
openpyxl>=3.1.0
python-dateutil>=2.8.0
PyYAML>=6.0
```

**packages.txt** (crear si necesitas paquetes del sistema):
```txt
# Agregar solo si necesitas paquetes específicos del sistema
```

---

### 🌐 OPCIÓN 2: Heroku (FREEMIUM)

#### 📋 Configuración para Heroku

1. **Crear archivos necesarios**

**Procfile**:
```
web: streamlit run dashboard_enterprise.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt**:
```
python-3.11.0
```

**setup.sh**:
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"tu-email@ejemplo.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

2. **Deploy a Heroku**
```bash
# Instalar Heroku CLI
# Desde: https://devcenter.heroku.com/articles/heroku-cli

# Login y crear app
heroku login
heroku create tu-dashboard-kpi

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

**URL**: `https://tu-dashboard-kpi.herokuapp.com/`

---

### ☁️ OPCIÓN 3: Google Cloud Platform

#### 📋 App Engine Deployment

**app.yaml**:
```yaml
runtime: python311

env_variables:
  STREAMLIT_SERVER_PORT: 8080
  STREAMLIT_SERVER_ADDRESS: 0.0.0.0

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

**Deploy**:
```bash
gcloud app deploy
```

---

### 🐳 OPCIÓN 4: Docker + Cloud Services

#### 📋 Dockerfile

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_enterprise.txt .
RUN pip install -r requirements_enterprise.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "dashboard_enterprise.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

**Deploy opciones**:
- **Digital Ocean**: $5/mes
- **AWS ECS**: Variable según uso
- **Google Cloud Run**: Pay per use
- **Azure Container Instances**: Variable

---

### 🔒 OPCIÓN 5: Con Autenticación (Enterprise)

#### 📋 Streamlit con Auth

**streamlit_authenticator** setup:
```python
# Agregar al inicio de dashboard_enterprise.py
import streamlit_authenticator as stauth

# Configuración de usuarios
names = ['Admin', 'Viewer']
usernames = ['admin', 'viewer']
passwords = ['admin123', 'viewer123']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'kpi_dashboard', 'secret_key', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:
    # Tu código del dashboard aquí
    main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
```

---

### 💰 COMPARACIÓN DE COSTOS

| Servicio | Costo | Límites | SSL | Dominio Custom |
|----------|-------|---------|-----|----------------|
| **Streamlit Cloud** | 🟢 Gratis | Moderados | ✅ | ❌ |
| **Heroku** | $7/mes | Buenos | ✅ | ✅ |
| **Google Cloud** | $5-20/mes | Altos | ✅ | ✅ |
| **Digital Ocean** | $5/mes | Buenos | ✅ | ✅ |
| **AWS** | $10-50/mes | Muy altos | ✅ | ✅ |

---

### 🚀 RECOMENDACIÓN PASO A PASO

#### Para Empezar RÁPIDO (5 minutos):

1. **Crear cuenta en GitHub** (si no tienes)
2. **Crear repositorio público** llamado `kpi-dashboard-enterprise`
3. **Subir todos los archivos** del proyecto
4. **Ir a Streamlit Cloud** (share.streamlit.io)
5. **Conectar repositorio** y deploy

#### Para Producción Profesional:

1. **Heroku** o **Google Cloud** para más control
2. **Dominio personalizado**: `dashboard.tuempresa.com`
3. **Autenticación** con usuarios específicos
4. **Base de datos real** en lugar de CSV
5. **Monitoreo** y analytics

---

### 🔧 PREPARACIÓN DE ARCHIVOS

#### Archivos que DEBES incluir para deployment:

✅ `dashboard_enterprise.py` (archivo principal)
✅ `requirements_enterprise.txt` (dependencias)
✅ `create_sample_data.py` (generador de datos)
✅ `data/samples/` (archivos CSV)
✅ `config/config.yaml` (configuración)
✅ `README_ENTERPRISE.md` (documentación)

#### Archivos opcionales pero recomendados:

🔄 `Procfile` (para Heroku)
🔄 `Dockerfile` (para containerización)
🔄 `app.yaml` (para Google Cloud)
🔄 `.streamlit/config.toml` (configuración específica)

---

### 📱 ACCESO MÓVIL

Tu dashboard será **automáticamente responsive** y funcionará en:
- 📱 **Móviles** (iOS/Android)
- 💻 **Tablets** (iPad, etc.)
- 🖥️ **Desktop** (todos los browsers)
- 📺 **TV displays** (para presentaciones)

---

### 🔐 SEGURIDAD

#### Para datos sensibles:
1. **Variables de entorno** para configuración
2. **Autenticación** obligatoria
3. **HTTPS** siempre habilitado
4. **Backup automático** de datos
5. **Logs de acceso** para auditoría

#### Archivo `.streamlit/secrets.toml`:
```toml
[database]
host = "tu-host-de-db"
username = "tu-usuario"
password = "tu-password"

[auth]
secret_key = "tu-clave-secreta"
```

---

### 📊 MONITOREO

#### Métricas que puedes trackear:
- **Usuarios únicos** por día
- **Tiempo de sesión** promedio
- **Páginas más visitadas**
- **Errores y performance**
- **Uso de recursos**

---

### 🎯 PRÓXIMOS PASOS SUGERIDOS

1. **Deployment inmediato**: Streamlit Cloud (gratis)
2. **Dominio personalizado**: Heroku + dominio propio
3. **Base de datos real**: PostgreSQL o MongoDB
4. **Autenticación**: Sistema de usuarios
5. **API REST**: Para integración con otros sistemas
6. **Mobile app**: React Native o Flutter
7. **Alertas por email**: Sistema de notificaciones

---

### 📞 SOPORTE POST-DEPLOYMENT

- **Logs**: `streamlit logs` para debug
- **Restart**: Redeploy automático en cada push
- **Scaling**: Automático según demanda
- **Backup**: GitHub mantiene historial completo

¿Te ayudo con alguna opción específica? ¡La más rápida es definitivamente Streamlit Cloud!