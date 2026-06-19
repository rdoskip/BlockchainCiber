import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generar_certificado_pki(nombre_alumno, correo_alumno):
    """
    Simula una Autoridad Certificadora (CA) académica o empresarial.
    Genera un par de claves criptográficas y un certificado X.509 autofirmado.
    """
    print(f"\n[PKI] Iniciando ciclo de vida del certificado para: {nombre_alumno}...")
    
    # 1. GENERACIÓN DE LA CLAVE PRIVADA (Algoritmo RSA de 2048 bits)
    print("[PKI] 1/3 Generando par de claves asimétricas RSA de 2048 bits...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # 2. CONFIGURACIÓN DE LOS METADATOS DEL CERTIFICADO X.509
    print("[PKI] 2/3 Estructurando metadatos e identidad del sujeto (X.509)...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"CO"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Santander"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Universidad de Seguridad"),
        x509.NameAttribute(NameOID.COMMON_NAME, nombre_alumno),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, correo_alumno),
    ])
    
    # Construcción y firma criptográfica del certificado digital (Válido por 1 año)
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
    
    # 3. SERIALIZACIÓN A FORMATO PEM
    print("[PKI] 3/3 Serializando certificado a formato estándar PEM...")
    cert_pem = certificado.public_bytes(serialization.Encoding.PEM)
    
    # Guardar físicamente el certificado en el almacenamiento local del servidor
    nombre_archivo = f"certificado_{nombre_alumno.replace(' ', '_')}.pem"
    with open(nombre_archivo, "wb") as f:
        f.write(cert_pem)
        
    print(f"[PKI] ¡Éxito! Archivo guardado correctamente como: {nombre_archivo}\n")
    return cert_pem