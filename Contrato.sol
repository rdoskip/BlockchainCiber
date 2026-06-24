// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Certificados {
    address public administrador;

    struct Certificado {
        string nombreAlumno;
        uint256 fechaRegistro;
        address emisor;
        bool existe;
    }

    mapping(bytes32 => Certificado) public certificados;

    event CertificadoRegistrado(
        bytes32 indexed hashCertificado,
        string nombreAlumno,
        address emisor
    );

    constructor() {
        administrador = msg.sender;
    }

    function registrarHashCertificado(bytes32 _hashCertificado, string memory _nombreAlumno) public {
        require(!certificados[_hashCertificado].existe, "El certificado ya esta registrado");
        
        certificados[_hashCertificado] = Certificado({
            nombreAlumno: _nombreAlumno,
            fechaRegistro: block.timestamp,
            emisor: msg.sender,
            existe: true
        });

        emit CertificadoRegistrado(_hashCertificado, _nombreAlumno, msg.sender);
    }

    function verificarCertificado(bytes32 _hashCertificado) public view returns (bool, string memory, uint256, address) {
        Certificado memory cert = certificados[_hashCertificado];
        return (cert.existe, cert.nombreAlumno, cert.fechaRegistro, cert.emisor);
    }
}
