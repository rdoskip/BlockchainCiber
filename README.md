# Ecosistema de Seguridad Unificado 🛡️

Este proyecto integra tres pilares fundamentales de la seguridad informática moderna: **Autenticación Multifactor (MFA)**, **Infraestructura de Clave Pública (PKI)** y la inmutabilidad de la tecnología **Blockchain**.

Desarrollado como trabajo final de grado, el sistema actúa como una Autoridad Certificadora (CA) simulada con una interfaz web moderna y segura. Emite certificados digitales `X.509` verificados y anclados a la blockchain para impedir su falsificación.

## 🚀 Características Principales

1. **Autenticación Perimetral Multifactor (MFA):**
   - Primer factor: Validación tradicional por credenciales.
   - Segundo factor: Tokens temporales basados en tiempo (TOTP) gestionados mediante una aplicación móvil (Google Authenticator, Authy, etc.).
   - Librería: `PyOTP`

2. **Emisión de Certificados Digitales (PKI):**
   - Generación de claves privadas RSA de 2048 bits.
   - Emisión de certificados bajo el estándar `X.509` con metadatos del estudiante/usuario.
   - Librería: `cryptography`

3. **Inmutabilidad y Auditoría (Blockchain):**
   - Cálculo del Hash Criptográfico (SHA-256) de cada certificado generado.
   - Interacción automatizada con un Smart Contract en Ethereum (entorno Ganache) para registrar el Hash.
   - Librería: `web3.py`

4. **Interfaz Web Premium (SPA):**
   - Panel administrativo moderno utilizando Vanilla CSS (diseño Glassmorphism y Dark Mode) y JavaScript puro (Llamadas API vía `fetch`), servido mediante Flask.

---

## 🛠️ Tecnologías y Requisitos

- **Python 3.8+**
- **Flask** (Backend Web)
- **Ganache** (Red Blockchain Local de Ethereum)
- **Web3.py** (Conexión Blockchain)
- **Cryptography** (Generación PKI)
- **PyOTP** (Manejo TOTP)

### Estructura del Proyecto

```text
/
├── app.py                     # Controlador principal backend (Flask, Web3, PKI)
├── pki_manager.py             # (Opcional) Funciones auxiliares criptográficas
├── templates/
│   └── index.html             # Interfaz Gráfica de Usuario (Web SPA)
├── static/
│   ├── style.css              # Estilos premium, animaciones, dark mode
│   └── app.js                 # Lógica del cliente, validaciones y conexión API
├── README.md                  # Este documento
└── requirements.txt           # Dependencias de Python
```

---

## ⚙️ Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/TU-USUARIO/ProyectoSeguridadUnificado.git
cd ProyectoSeguridadUnificado
```

### 2. Entorno Virtual y Dependencias
Se recomienda utilizar un entorno virtual (`venv`):
```bash
python -m venv venv
# Activar en Windows
venv\Scripts\activate
# Activar en macOS/Linux
source venv/bin/activate

pip install Flask cryptography web3 pyotp
```

### 3. Configurar Ganache (Blockchain)
1. Descarga e instala [Ganache](https://trufflesuite.com/ganache/).
2. Inicia un Workspace rápido ("Quickstart"). Ganache correrá en `http://127.0.0.1:7545`.
3. Despliega el Smart Contract compilado (usando Remix IDE, Hardhat o Truffle).
4. Copia la **Dirección del Contrato Desplegado** (Contract Address).
5. Abre el archivo `app.py` y actualiza la constante `CONTRATO_ADDRESS` con tu nueva dirección.

---

## 💻 Uso de la Aplicación

1. **Iniciar el Servidor Flask:**
```bash
python app.py
```

para revisar la informacion del contrato puedes usar el script ver_enventos.py con python ver_eventos.py

> **Nota:** En la consola verás una advertencia de "CONFIGURACIÓN AUTOMÁTICA DE TU DISPOSITIVO MÓVIL". Ese link URI puedes ignorarlo si planeas escanear el QR directamente desde la interfaz web.

2. **Abrir el Panel de Control:**
   - Dirígete a `http://127.0.0.1:5000` en tu navegador.
   
3. **Flujo de Seguridad:**
   - **Paso 1:** Ingresa con las credenciales por defecto (`admin@universidad.edu` / `admin123`).
   - **Paso 2:** Si es tu primera vez, escanea el código QR que aparecerá en pantalla con Google Authenticator. Luego ingresa el PIN de 6 dígitos que genera la app móvil.
   - **Paso 3:** Una vez desbloqueada la consola, ingresa el nombre y correo institucional de un estudiante.
   - **Paso 4:** Haz clic en "Generar y Anclar a Blockchain". Observa la Consola de Auditoría Integrada y cómo se genera físicamente el archivo `.pem` en la carpeta raíz del proyecto.

---

## 🤝 Contribuciones y Conclusiones
Este prototipo es una prueba de concepto (PoC) académica que demuestra cómo la Defensa en Profundidad (MFA + PKI + Blockchain) previene de manera efectiva vulnerabilidades críticas como el robo de sesión y falsificación de documentación sensible en sistemas de acreditación y certificación.
