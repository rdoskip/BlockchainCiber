import os
from web3 import Web3

# 1. Configuración de conexión a Ganache
BLOCKCHAIN_PROVIDER = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_PROVIDER))

# 2. Dirección y ABI del Contrato (Mismos que en app.py)
CONTRATO_ADDRESS = "0x4Da004c24BD038D6577D694063ef543b4ccB8D78"
CONTRATO_ABI = [
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
    }
]

def ver_eventos_registrados():
    if not w3.is_connected():
        print("❌ Error: No se pudo conectar a Ganache. ¿Está ejecutándose?")
        return

    print("✅ Conectado a Ganache.")
    print(f"Buscando eventos en el contrato: {CONTRATO_ADDRESS}\n")

    try:
        contrato = w3.eth.contract(address=CONTRATO_ADDRESS, abi=CONTRATO_ABI)
        
        # Filtrar todos los eventos 'CertificadoRegistrado' desde el bloque 0 hasta el último
        eventos = contrato.events.CertificadoRegistrado.create_filter(
    from_block=0,
    to_block='latest'
).get_all_entries()
        
        if not eventos:
            print("No se encontró ningún certificado registrado en la Blockchain todavía.")
            return

        print("-" * 70)
        print(f"🎓 SE HAN ENCONTRADO {len(eventos)} CERTIFICADOS REGISTRADOS 🎓")
        print("-" * 70)

        for evento in eventos:
            # Extraer los datos del evento
            args = evento['args']
            hash_cert = args['hashCertificado'].hex()
            alumno = args['nombreAlumno']
            emisor = args['emisor']
            bloque = evento['blockNumber']
            tx_hash = evento['transactionHash'].hex()

            print(f"🔹 Alumno: {alumno}")
            print(f"   Bloque: {bloque}")
            print(f"   Hash del Certificado: {hash_cert}")
            print(f"   Emisor (Cuenta Ganache): {emisor}")
            print(f"   Transacción: {tx_hash}")
            print("-" * 70)

    except Exception as e:
        print(f"❌ Error al consultar la Blockchain: {e}")

if __name__ == '__main__':
    ver_eventos_registrados()
