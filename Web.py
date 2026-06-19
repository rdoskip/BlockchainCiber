import os
from web3 import Web3

class BlockchainManager:
    def __init__(self, provider_url, contract_address, contract_abi):
        """
        Inicializa la conexión con el nodo Blockchain y mapea el Smart Contract.
        """
        # Conectar al proveedor de la red local (Ganache o la red virtual de Remix)
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_address = contract_address
        self.contract_abi = contract_abi
        self.contract = None
        
        # Verificar estado de la conexión al inicializar
        if self.w3.is_connected():
            print(f"[BLOCKCHAIN] Conectado exitosamente al nodo: {provider_url}")
            # Instanciar el objeto del contrato inteligente
            self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        else:
            print("[BLOCKCHAIN] ¡Advertencia! No se pudo establecer conexión con el nodo Blockchain.")

    def registrar_hash_en_blockchain(self, hash_hex, nombre_alumno):
        """
        Envía una transacción al Smart Contract para guardar la huella digital (hash)
        del certificado de manera completamente inmutable y descentralizada.
        """
        if not self.w3.is_connected() or self.contract is None:
            raise Exception("No hay conexión activa con la red Blockchain o el contrato no está instanciado.")
            
        print(f"[BLOCKCHAIN] Preparando transacción para registrar el hash del alumno: {nombre_alumno}...")

        try:
            # 1. Convertir el hash SHA-256 en formato hexadecimal de Python a formato bytes32 de Solidity
            hash_bytes32 = self.w3.to_bytes(hexstr=hash_hex)
            
            # 2. Seleccionar la cuenta que pagará el Gas de la transacción (por defecto la primera de Ganache/Remix)
            cuenta_administrador = self.w3.eth.accounts[0]
            
            # 3. Invocar la función del Smart Contract y enviar la transacción
            print("[BLOCKCHAIN] Enviando transacción al Smart Contract...")
            tx_hash = self.contract.functions.registrarHashCertificado(
                hash_bytes32, 
                nombre_alumno
            ).transact({'from': cuenta_administrador})
            
            # 4. Esperar de forma síncrona a que la red valide y mine el bloque de la transacción
            print("[BLOCKCHAIN] En proceso de minado. Esperando confirmación...")
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"[BLOCKCHAIN] Transacción confirmada con éxito en el bloque número: {tx_receipt.blockNumber}")
            return {
                "bloque": tx_receipt.blockNumber,
                "tx_id": tx_hash.hex(),
                "remitente": cuenta_administrador
            }
            
        except Exception as e:
            print(f"[BLOCKCHAIN] Error crítico durante la transacción: {str(e)}")
            raise e