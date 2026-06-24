document.addEventListener('DOMContentLoaded', () => {
    // Referencias a paneles
    const panelLogin = document.getElementById('panel-login');
    const panelMfa = document.getElementById('panel-mfa');
    const panelPki = document.getElementById('panel-pki');

    // Referencias a alertas
    const alertLogin = document.getElementById('alert-login');
    const alertMfa = document.getElementById('alert-mfa');
    const alertPki = document.getElementById('alert-pki');

    function showAlert(element, message, type = 'error') {
        element.textContent = message;
        element.className = `alert ${type}`;
    }

    function hideAlert(element) {
        element.className = 'alert';
    }

    if (typeof mfaUri !== 'undefined' && mfaUri && document.getElementById("qrcode")) {
        new QRCode(document.getElementById("qrcode"), {
            text: mfaUri,
            width: 130,
            height: 130,
            colorDark : "#0f172a",
            colorLight : "#ffffff",
            correctLevel : QRCode.CorrectLevel.M
        });
    }

    function switchPanel(hidePanel, showPanel) {
        hidePanel.classList.remove('active');
        setTimeout(() => {
            showPanel.classList.add('active');
        }, 300);
    }

    // --- FORMULARIO LOGIN ---
    document.getElementById('form-login').addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('btn-login');
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-pass').value;

        hideAlert(alertLogin);
        btn.classList.add('loading');
        btn.disabled = true;

        try {
            const fd = new FormData();
            fd.append('email', email);
            fd.append('password', password);

            const res = await fetch('/login', { method: 'POST', body: fd });
            const data = await res.json();

            if (res.ok) {
                switchPanel(panelLogin, panelMfa);
            } else {
                showAlert(alertLogin, data.error || 'Credenciales inválidas');
            }
        } catch (err) {
            showAlert(alertLogin, 'Error de conexión con el servidor.');
        } finally {
            btn.classList.remove('loading');
            btn.disabled = false;
        }
    });

    // --- FORMULARIO MFA ---
    document.getElementById('form-mfa').addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('btn-mfa');
        const token = document.getElementById('mfa-token').value;

        hideAlert(alertMfa);
        btn.classList.add('loading');
        btn.disabled = true;

        try {
            const fd = new FormData();
            fd.append('token', token);

            const res = await fetch('/verificar-mfa', { method: 'POST', body: fd });
            const data = await res.json();

            if (res.ok) {
                switchPanel(panelMfa, panelPki);
            } else {
                showAlert(alertMfa, data.error || 'Token incorrecto');
            }
        } catch (err) {
            showAlert(alertMfa, 'Error de conexión.');
        } finally {
            btn.classList.remove('loading');
            btn.disabled = false;
        }
    });

    // --- FORMULARIO EMISIÓN ---
    document.getElementById('form-pki').addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('btn-pki');
        const nombre = document.getElementById('pki-nombre').value;
        const correo = document.getElementById('pki-correo').value;
        const consoleLog = document.getElementById('console-log');

        hideAlert(alertPki);
        btn.classList.add('loading');
        btn.disabled = true;
        consoleLog.textContent = "> Generando certificado e interactuando con Blockchain...\n> Por favor espera...";

        try {
            const fd = new FormData();
            fd.append('nombre', nombre);
            fd.append('correo', correo);

            const res = await fetch('/emitir-certificado', { method: 'POST', body: fd });
            const data = await res.json();

            if (res.ok) {
                showAlert(alertPki, 'Certificado emitido e indexado con éxito.', 'success');
                
                let text = `> [PKI] Estado: ${data.estado}\n`;
                text += `> [ALUMNO]: ${data.alumno}\n`;
                text += `> [MENSAJE]: ${data.mensaje}\n`;
                text += `> [HASH SHA-256]: ${data.sha256_hash}\n`;
                text += `> [BLOCKCHAIN]: Bloque ${data.blockchain_bloque}\n`;
                text += `> [NODO DATA]: TX ${data.transaccion_tx}\n`;
                
                consoleLog.textContent = text;
            } else {
                showAlert(alertPki, data.error || data.estado || 'Fallo en la emisión.');
                consoleLog.textContent = "> Error:\n" + JSON.stringify(data, null, 2);
            }
        } catch (err) {
            showAlert(alertPki, 'Error de conexión con la arquitectura.');
            consoleLog.textContent = "> Error interno: " + err.message;
        } finally {
            btn.classList.remove('loading');
            btn.disabled = false;
        }
    });
});
