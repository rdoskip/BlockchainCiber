import os
import datetime
import hashlib
import pyotp
from flask import Flask, request, redirect, session, jsonify, render_template
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from web3 import Web3

# ==========================================
# 1. CONFIGURACIÓN INICIAL Y BASE DE DATOS SIMULADA
# ==========================================
app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# Base de datos en memoria para testing académico
USUARIOS_DB = {
    "admin@universidad.edu": {
        "password_hash": "admin123",
        "mfa_secret": pyotp.random_base32()
    }
}

# ==========================================
# 2. CAPA DE IDENTIDAD (PKI - GENERACIÓN DE CERTIFICADOS)
# ==========================================
def generar_certificado_pki(nombre_alumno, correo_alumno):
    """
    Simula una Autoridad Certificadora (CA) local emitiendo un certificado digital X.509.
    """
    # Generar la Clave Privada del Alumno
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    # Estructurar metadatos del certificado X.509
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"CO"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Santander"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Universidad de Seguridad"),
        x509.NameAttribute(NameOID.COMMON_NAME, nombre_alumno),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, correo_alumno),
    ])
    
    # Construcción del certificado válido por 1 año
    certificado = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).sign(private_key, hashes.SHA256())
    
    # Serializar el certificado a formato PEM
    cert_pem = certificado.public_bytes(serialization.Encoding.PEM)
    
    # Guardar una copia física local del certificado generado
    nombre_archivo = f"certificado_{nombre_alumno.replace(' ', '_')}.pem"
    with open(nombre_archivo, "wb") as f:
        f.write(cert_pem)
        
    return cert_pem

# ==========================================
# 3. CAPA CORE (CONEXIÓN A LA BLOCKCHAIN CON WEB3)
# ==========================================

# Conectar a Ganache
BLOCKCHAIN_PROVIDER = "http://127.0.0.1:7545"  # Puerto por defecto de Ganache
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_PROVIDER))

# Verificar conexión
if w3.is_connected():
    print("✅ Conectado a Ganache en", BLOCKCHAIN_PROVIDER)
    print(f"Cuentas disponibles: {w3.eth.accounts}")
else:
    print("❌ No se pudo conectar a Ganache. Verifica que esté ejecutándose.")
    exit(1)

# REEMPLAZAR con tu dirección de contrato desplegado en Ganache
CONTRATO_ADDRESS = "0x4Da004c24BD038D6577D694063ef543b4ccB8D78"  # ¡ACTUALIZA ESTA DIRECCIÓN!

# ABI del contrato - CORREGIDO (solo el array, no anidado)
CONTRATO_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "hashCertificado",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "nombreAlumno",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "emisor",
                "type": "address"
            }
        ],
        "name": "CertificadoRegistrado",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_hashCertificado",
                "type": "bytes32"
            },
            {
                "internalType": "string",
                "name": "_nombreAlumno",
                "type": "string"
            }
        ],
        "name": "registrarHashCertificado",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "administrador",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "name": "certificados",
        "outputs": [
            {
                "internalType": "string",
                "name": "nombreAlumno",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "fechaRegistro",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "emisor",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "existe",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_hashCertificado",
                "type": "bytes32"
            }
        ],
        "name": "verificarCertificado",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Instanciar el contrato
try:
    contrato_blockchain = w3.eth.contract(address=CONTRATO_ADDRESS, abi=CONTRATO_ABI)
    print("✅ Contrato cargado correctamente")
except Exception as e:
    print(f"❌ Error cargando el contrato: {e}")
    contrato_blockchain = None

# ==========================================
# 4. RUTAS DEL CONTROLADOR WEB (FLASK API)
# ==========================================

@app.route('/')
def home():
    usuario_test = "admin@universidad.edu"
    secreto_test = USUARIOS_DB[usuario_test]["mfa_secret"]
    totp_config = pyotp.TOTP(secreto_test)
    uri_totp = totp_config.provisioning_uri(name=usuario_test, issuer_name="Universidad-Core-Seguridad")
    return render_template('index.html', mfa_uri=uri_totp)

@app.route('/login', methods=['POST'])
def login():
    """
    Primer Factor de Autenticación: Valida usuario y contraseña tradicionales.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    usuario = USUARIOS_DB.get(email)
    if usuario and usuario['password_hash'] == password:
        session['pre_auth_email'] = email
        return jsonify({
            "estado": "Primer factor aprobado", 
            "mensaje": "Por favor, proceda a la verificación del token MFA en /verificar-mfa"
        }), 200
    
    return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/verificar-mfa', methods=['POST'])
def verificar_mfa():
    """
    Segundo Factor de Autenticación: Valida el código TOTP de 6 dígitos.
    """
    email = session.get('pre_auth_email')
    if not email:
        return jsonify({"error": "Debe iniciar sesión primero en /login"}), 403
        
    token = request.form.get('token')
    usuario = USUARIOS_DB.get(email)
    
    totp = pyotp.TOTP(usuario['mfa_secret'])
    
    if totp.verify(token):
        session['user_email'] = email
        session.pop('pre_auth_email', None)
        return jsonify({"estado": "MFA Verificado", "mensaje": "Bienvenido al sistema seguro"}), 200
        
    return jsonify({"error": "Token MFA incorrecto o expirado"}), 401

@app.route('/emitir-certificado', methods=['POST'])
def emitir_certificado():
    """
    Acción Protegida: Genera el certificado físico (PKI) y registra su huella digital en Blockchain.
    """
    if 'user_email' not in session:
        return jsonify({"error": "Acceso denegado. Requiere autenticación MFA activa."}), 401
        
    nombre_alumno = request.form.get('nombre')
    correo_alumno = request.form.get('correo')
    
    if not nombre_alumno or not correo_alumno:
        return jsonify({"error": "Faltan parámetros requeridos (nombre, correo)"}), 400
        
    try:
        # FASE PKI: Generar certificado digital X.509
        certificado_pem = generar_certificado_pki(nombre_alumno, correo_alumno)
        
        # FASE CRIPTOGRAFÍA: Calcular el hash SHA-256
        hash_certificado = hashlib.sha256(certificado_pem).hexdigest()
        hash_bytes32 = bytes.fromhex(hash_certificado)  # Convertir hex a bytes
        
        # FASE BLOCKCHAIN: Interacción con el Smart Contract
        if contrato_blockchain is None:
            return jsonify({
                "estado": "Advertencia",
                "archivo_pki": "Certificado PEM creado localmente",
                "hash_local": hash_certificado,
                "blockchain": "Error: Contrato no disponible"
            }), 500
            
        # Usar la primera cuenta de Ganache
        cuenta_admin = w3.eth.accounts[0]
        
        # Verificar que la cuenta tiene ETH
        balance = w3.eth.get_balance(cuenta_admin)
        print(f"Balance de {cuenta_admin}: {w3.from_wei(balance, 'ether')} ETH")
        
        # Construir y enviar transacción
        tx = contrato_blockchain.functions.registrarHashCertificado(
            hash_bytes32, 
            nombre_alumno
        ).build_transaction({
            'from': cuenta_admin,
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(cuenta_admin)
        })
        
        # Firmar y enviar transacción
        # NOTA: En producción, no deberías tener la clave privada en texto plano
        # Para pruebas con Ganache, usa una de las cuentas predeterminadas
        # o desbloquea una cuenta
        
        # Para Ganache, podemos enviar directamente sin firmar (ya que está desbloqueado)
        # O podemos usar la clave privada de la primera cuenta
        # Obtener clave privada de la primera cuenta de Ganache (si está disponible)
        # En Ganache, las claves privadas se muestran en la interfaz
        
        # Opción 1: Si Ganache tiene cuentas desbloqueadas
        tx_hash = w3.eth.send_transaction(tx)
        
        # Opción 2: Si necesitas firmar manualmente (descomenta si es necesario)
        # private_key = "0x..."  # Tu clave privada de Ganache
        # signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        # tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Esperar confirmación
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return jsonify({
            "estado": "Éxito Absoluto",
            "mensaje": "Certificado protegido e inmutable",
            "alumno": nombre_alumno,
            "sha256_hash": hash_certificado,
            "blockchain_bloque": tx_receipt.blockNumber,
            "transaccion_tx": tx_hash.hex()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Fallo interno en el proceso: {str(e)}"}), 500

# ==========================================
# 5. INICIALIZADOR AUTOMÁTICO DE ENTORNO MFA
# ==========================================
if __name__ == '__main__':
    usuario_test = "admin@universidad.edu"
    secreto_test = USUARIOS_DB[usuario_test]["mfa_secret"]
    totp_config = pyotp.TOTP(secreto_test)
    
    uri_totp = totp_config.provisioning_uri(name=usuario_test, issuer_name="Universidad-Core-Seguridad")
    
    print("\n" + "="*70)
    print(" CONFIGURACIÓN AUTOMÁTICA DE TU DISPOSITIVO MÓVIL (MFA)")
    print("="*70)
    print(f"Usuario de pruebas: {usuario_test}")
    print(f"Contraseña: {USUARIOS_DB[usuario_test]['password_hash']}")
    print("\nCopia y pega la siguiente URI en un generador de códigos QR online:")
    print(f"\033[94m{uri_totp}\033[0m")
    print("\nO escanea este código QR con Google Authenticator o Authy")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5000)