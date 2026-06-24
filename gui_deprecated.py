import tkinter as tk
from tkinter import ttk, messagebox
import requests

# URL base del servidor Flask que ya tienes corriendo
BASE_URL = "http://127.0.0.1:5000"

class SistemaSeguridadGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ecosistema de Seguridad Unificado")
        self.root.geometry("600x500")
        self.session = requests.Session() # Mantiene las cookies de sesión (MFA) activa

        # Título Principal
        titulo = tk.Label(root, text="Panel de Control de Seguridad Criptográfica", font=("Arial", 16, "bold"), fg="#1a365d")
        titulo.pack(pady=10)

        # Contenedor de Pestañas (Notebook)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear las 3 pestañas basadas en tus propuestas
        self.tab_mfa = ttk.Frame(self.notebook)
        self.tab_pki_blockchain = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_mfa, text="1. Autenticación Perimetral (MFA)")
        self.notebook.add(self.tab_pki_blockchain, text="2. Emisión (PKI + Blockchain)")
        
        # Deshabilitar la segunda pestaña al inicio por seguridad
        self.notebook.tab(1, state="disabled")

        self.inicializar_tab_mfa()
        self.inicializar_tab_pki()

    # ==========================================
    # INTERFAZ FASE 1: MULTIFACTOR AUTH
    # ==========================================
    def inicializar_tab_mfa(self):
        # Campos Login
        tk.Label(self.tab_mfa, text="Correo Administrador:", font=("Arial", 10, "bold")).pack(pady=5)
        self.txt_email = tk.Entry(self.tab_mfa, width=40)
        self.txt_email.insert(0, "admin@universidad.edu")
        self.txt_email.pack()

        tk.Label(self.tab_mfa, text="Contraseña:", font=("Arial", 10, "bold")).pack(pady=5)
        self.txt_pass = tk.Entry(self.tab_mfa, show="*", width=40)
        self.txt_pass.insert(0, "admin123")
        self.txt_pass.pack()

        btn_login = tk.Button(self.tab_mfa, text="Validar Primer Factor", command=self.ejecutar_login, bg="#2b6cb0", fg="white", font=("Arial", 10, "bold"))
        btn_login.pack(pady=10)

        # Campo Token OTP
        self.lbl_token = tk.Label(self.tab_mfa, text="Ingrese Token de su Celular (Google Authenticator):", font=("Arial", 10, "bold"), state="disabled")
        self.lbl_token.pack(pady=5)
        self.txt_token = tk.Entry(self.tab_mfa, width=20, state="disabled", justify="center", font=("Arial", 12))
        self.txt_token.pack()

        self.btn_mfa = tk.Button(self.tab_mfa, text="Verificar Código MFA", command=self.ejecutar_mfa, bg="#2f855a", fg="white", font=("Arial", 10, "bold"), state="disabled")
        self.btn_mfa.pack(pady=10)

    def ejecutar_login(self):
        payload = {"email": self.txt_email.get(), "password": self.txt_pass.get()}
        try:
            r = self.session.post(f"{BASE_URL}/login", data=payload)
            if r.status_code == 200:
                messagebox.showinfo("Éxito", "Primer factor aprobado. Ingrese el código OTP de su celular.")
                self.lbl_token.config(state="normal")
                self.txt_token.config(state="normal")
                self.btn_mfa.config(state="normal")
            else:
                messagebox.showerror("Error", r.json().get("error", "Credenciales incorrectas"))
        except Exception as e:
            messagebox.showerror("Error de Red", f"¿Encendiste app.py? No hay conexión: {str(e)}")

    def ejecutar_mfa(self):
        payload = {"token": self.txt_token.get()}
        r = self.session.post(f"{BASE_URL}/verificar-mfa", data=payload)
        if r.status_code == 200:
            messagebox.showinfo("Acceso Concedido", "MFA Verificado. Se ha desbloqueado la zona de emisión.")
            self.notebook.tab(1, state="normal") # Desbloquea la pestaña de emisión
            self.notebook.select(1) # Cambia automáticamente de pestaña
        else:
            messagebox.showerror("Error", "Token incorrecto o expirado. Intente de nuevo.")

    # ==========================================
    # INTERFAZ FASE 2 Y 3: PKI + BLOCKCHAIN
    # ==========================================
    def inicializar_tab_pki(self):
        tk.Label(self.tab_pki_blockchain, text="Nombre Completo del Alumno:", font=("Arial", 10, "bold")).pack(pady=5)
        self.txt_alumno = tk.Entry(self.tab_pki_blockchain, width=45)
        self.txt_alumno.pack()

        tk.Label(self.tab_pki_blockchain, text="Correo Electrónico Institucional:", font=("Arial", 10, "bold")).pack(pady=5)
        self.txt_correo_alumno = tk.Entry(self.tab_pki_blockchain, width=45)
        self.txt_correo_alumno.pack()

        btn_emitir = tk.Button(self.tab_pki_blockchain, text="Generar Certificado Firme y Anclar a Blockchain", command=self.ejecutar_emision, bg="#c53030", fg="white", font=("Arial", 10, "bold"))
        btn_emitir.pack(pady=15)

        # Cuadro de resultados técnicos
        tk.Label(self.tab_pki_blockchain, text="Consola de Auditoría Criptográfica:", font=("Arial", 9, "italic")).pack()
        self.txt_log = tk.Text(self.tab_pki_blockchain, height=10, width=65, bg="#edf2f7", font=("Courier", 9))
        self.txt_log.pack(pady=5)

    def ejecutar_emision(self):
        payload = {"nombre": self.txt_alumno.get(), "correo": self.txt_correo_alumno.get()}
        r = self.session.post(f"{BASE_URL}/emitir-certificado", data=payload)
        
        self.txt_log.delete("1.0", tk.END) # Limpiar consola visual
        if r.status_code == 200:
            data = r.json()
            # Formatear la respuesta JSON en la pantalla de la GUI
            texto_resultado = f"[PKI] Estado: {data.get('estado')}\n"
            texto_resultado += f"[ALUMNO]: {data.get('alumno')}\n"
            texto_resultado += f"[MENSAJE]: {data.get('mensaje')}\n"
            texto_resultado += f"[HASH SHA-256]: {data.get('sha256_hash')}\n"
            texto_resultado += f"[BLOCKCHAIN]: Bloque {data.get('blockchain_bloque')}\n"
            texto_resultado += f"[NODO DATA]: TX {data.get('transaccion_tx')}\n"
            self.txt_log.insert(tk.END, texto_resultado)
            messagebox.showinfo("Proceso Terminado", "Certificado emitido e indexado con éxito.")
        else:
            self.txt_log.insert(tk.END, f"Error en la arquitectura: {r.text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaSeguridadGUI(root)
    root.mainloop()