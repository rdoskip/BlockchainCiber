# Prompt / Base de Contexto para Generación del Documento Final (PDF 10-12 páginas)

**Instrucción para el LLM (Claude/ChatGPT):** 
Actúa como un experto en Seguridad Informática y redactor académico. Utiliza el siguiente esquema y contexto técnico para redactar un informe final de proyecto universitario de entre 10 y 12 páginas. El proyecto integra tres pilares: Autenticación Multifactor (MFA), Infraestructura de Clave Pública (PKI) y Blockchain.

---

## 1. Título del proyecto y descripción general
**Título Sugerido:** Ecosistema de Seguridad Unificado: Integración de MFA, Infraestructura PKI y Blockchain para la Emisión Inmutable de Certificados Digitales.
**Descripción General:**
El proyecto consiste en el diseño e implementación de un prototipo funcional web desarrollado en Python (Flask) que integra múltiples capas de seguridad informática. El sistema actúa como una Autoridad Certificadora (CA) interna que emite certificados digitales X.509 para estudiantes. Para proteger el acceso al panel de emisión, se implementó una Autenticación Multifactor (MFA) perimetral (Credenciales + TOTP mediante Google Authenticator). Además, para garantizar la inmutabilidad y evitar la falsificación de los certificados emitidos, el hash criptográfico (SHA-256) de cada certificado generado se registra en una red Blockchain local (Ethereum/Ganache) mediante un Smart Contract.

## 2. Problema identificado y justificación del uso de MFA
**Problema:** Las instituciones educativas e corporativas sufren constantes vulnerabilidades por robo de credenciales, ataques de phishing y falsificación de diplomas o certificados. Una CA tradicional protegida únicamente por un usuario y contraseña es un punto único de falla sumamente vulnerable; si un atacante obtiene esas credenciales, puede emitir certificados falsos indiscriminadamente.
**Justificación MFA:** Implementar MFA (Multi-Factor Authentication) mitiga drásticamente este riesgo al exigir, además de "algo que el usuario sabe" (contraseña), "algo que el usuario tiene" (su dispositivo móvil con la app Google Authenticator). Así, incluso si las credenciales son comprometidas, el atacante no podrá acceder al sistema de emisión PKI sin el código temporal (TOTP) de 6 dígitos que cambia cada 30 segundos.

## 3. Objetivo general y objetivos específicos
**Objetivo General:**
Desarrollar un prototipo de plataforma web segura orientada a la gestión y emisión de certificados digitales, integrando controles de acceso mediante MFA y garantizando la integridad de los documentos a través de la inmutabilidad de la tecnología Blockchain.

**Objetivos Específicos:**
1. Diseñar e implementar un esquema de Autenticación Multifactor (MFA) combinando validación tradicional y tokens TOTP para proteger recursos críticos.
2. Construir un módulo PKI (Public Key Infrastructure) capaz de generar pares de claves RSA y emitir certificados digitales X.509 válidos.
3. Desarrollar e integrar un Contrato Inteligente (Smart Contract) en una red Blockchain (Ethereum/Ganache) para anclar y registrar los hashes criptográficos de los certificados emitidos.
4. Evaluar la arquitectura del prototipo como base para una futura Autoridad Certificadora (CA) robusta, analizando sus capacidades para el ciclo de vida de los certificados.

## 4. Diagrama de arquitectura propuesta (componentes y flujos de datos)
*(Nota para la redacción: Describir este flujo detalladamente para que el estudiante pueda generar un diagrama visual posteriormente)*
**Componentes:**
- **Frontend Web:** HTML, Vanilla CSS (Glassmorphism), Vanilla JS.
- **Backend API:** Servidor Python con Flask.
- **Módulo de Identidad:** PyOTP (para generación/validación de TOTP MFA).
- **Módulo PKI:** Librería `cryptography` de Python para RSA y X.509.
- **Módulo Blockchain:** Librería `web3.py` conectada a un nodo RPC de Ganache.
- **Smart Contract:** Escrito en Solidity, con la función `registrarHashCertificado(bytes32, string)`.

**Flujo de Datos (Arquitectura):**
1. **Paso de Autenticación:** El cliente envía credenciales (POST /login) -> El backend valida en base de datos -> Devuelve éxito e invita al segundo factor.
2. **Paso MFA:** El cliente escanea el QR y envía el token TOTP (POST /verificar-mfa) -> Backend valida con `PyOTP` -> Se crea la sesión segura `user_email`.
3. **Paso de Emisión:** El administrador autorizado envía datos del estudiante (POST /emitir-certificado) -> El backend genera llave privada RSA y emite el archivo PEM (Certificado X.509).
4. **Paso de Inmutabilidad:** El backend calcula el SHA-256 del PEM generado -> Web3.py arma la transacción y la envía al contrato en Ganache -> Ganache mina el bloque y devuelve el hash de la transacción (Tx Hash).

## 5. Herramientas tecnológicas seleccionadas
- **Python & Flask:** Lenguaje y framework principal por su agilidad y ricas librerías de ciberseguridad.
- **PyOTP:** Para la generación de URIs de aprovisionamiento (códigos QR) y la verificación algorítmica de los tokens de tiempo.
- **Cryptography (Python):** Para la gestión de criptografía asimétrica, generación de claves RSA de 2048 bits y la estructuración formal del estándar X.509.
- **Web3.py & Ganache:** Para la simulación de la red Ethereum local y la interacción (firma de transacciones e invocación de métodos) con el Smart Contract.
- **HTML/CSS/JS nativo:** Para construir una interfaz "Single Page Application" ligera, rápida y estéticamente moderna sin dependencias pesadas.

## 6. Evaluación breve de resultados

### Análisis desde el punto de vista de posibilidad de ser autoridad certificadora (CA) y contribución al ciclo de vida
El prototipo implementado cumple de manera excepcional con la fase inicial del **ciclo de vida de un certificado**: el aprovisionamiento y emisión. Actúa como una CA local válida porque estructura correctamente los atributos del sujeto (país, organización, email) firmándolos bajo un estándar reconocido (X.509). La integración con Blockchain elimina la necesidad de depender de una única base de datos tradicional para auditar la validez; cualquier tercero puede calcular el hash del certificado (.pem) de un estudiante y buscarlo en el Smart Contract para probar matemáticamente que fue emitido por esta CA y no ha sido alterado. Esto descentraliza la capa de verificación.

### Limitaciones y posibles mejoras en pro de tener una Autoridad Certificadora (CA) real
- **Gestión de Revocación (CRL / OCSP):** Actualmente el sistema emite certificados pero carece de un mecanismo formal para revocarlos (por ejemplo, si se compromete la clave del estudiante). Una mejora vital sería implementar Listas de Revocación de Certificados o un protocolo OCSP, y registrar dicha revocación también en la Blockchain.
- **Almacenamiento Seguro (HSM):** La clave privada de la CA (que firma los certificados) y las credenciales de la billetera Blockchain están manejadas de forma lógica en software. Una CA de grado militar requeriría un *Hardware Security Module (HSM)* para salvaguardar el material criptográfico maestro.
- **Gestión de Sesiones y Trazabilidad de Auditoría:** Agregar un esquema de roles más robusto (RBAC) y un log inmutable de todos los intentos de acceso y emisión, posiblemente utilizando herramientas estilo HashiCorp Vault.

## 7. Conclusiones generales del equipo
- La integración de un factor de autenticación basado en "algo que tienes" (TOTP) erradica vectores de ataque fundamentales, probando ser una barrera altamente efectiva para sistemas de emisión crítica.
- La convergencia entre PKI tradicional y Blockchain resuelve el problema de la "confianza centralizada", brindando un registro inmutable que facilita la auditoría transparente sin exponer los datos sensibles de los usuarios en texto plano (se exponen únicamente hashes matemáticos).
- El proyecto demuestra que la seguridad informática moderna no recae en una sola tecnología o barrera, sino en la **Defensa en Profundidad**: MFA para el acceso, PKI para la identidad y confidencialidad del dato, y Blockchain para la integridad y no repudio del registro histórico.
