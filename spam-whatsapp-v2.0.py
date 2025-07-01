import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.font as tkfont
import pyautogui
import pyperclip
import time
import threading
import sys
import os
import unicodedata
import re

class AutoMensajesPro:
    def __init__(self):
        self.root = tk.Tk()
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.enviando = False
        self.thread_activo = None

        # Configurar pyautogui desde el inicio
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.02  # Pausa más conservadora para mayor estabilidad

        self.setup_ui()
        self.log("🚀 Auto Mensajes Pro v2.0 iniciado correctamente")
        self.log("🔧 Método Portapapeles + Ctrl+V para máxima compatibilidad")

    # Configuración de la interfaz de usuario
    def setup_ui(self):
        self.root.title("🚀 Auto Mensajes Pro v2.0")
        self.root.geometry("750x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.modo_linea_por_linea = tk.BooleanVar(value=False)
        self.metodo_envio = tk.StringVar(
            value="portapapeles")  # portapapeles o typewrite

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')

        # Frame principal con padding
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(padx=15, pady=15, fill="both", expand=True)

        # SECCIÓN 1: Mensaje
        self.create_message_section(main_frame)

        # SECCIÓN 2: Configuración
        self.create_config_section(main_frame)

        # SECCIÓN 3: Control
        self.create_control_section(main_frame)

        # SECCIÓN 4: Estado y Log
        self.create_status_section(main_frame)

    def create_message_section(self, parent):
        """Sección para configurar el mensaje"""
        frame = tk.LabelFrame(parent, text="📝 MENSAJE A ENVIAR",
                              font=("Arial", 11, "bold"), bg="#f0f0f0", fg="#2c3e50")
        frame.pack(fill="x", pady=(0, 10))

        # Texto del mensaje
        tk.Label(frame, text="Escribe tu mensaje aquí (soporta tildes, emojis y caracteres especiales):",
                 font=("Arial", 9), bg="#f0f0f0").pack(anchor="w", padx=10, pady=(10, 5))

        self.text_mensaje = tk.Text(frame, width=85, height=8,
                                    font=("Consolas", 10), relief="solid", bd=1,
                                    wrap=tk.WORD)  # Wrap mejorado
        self.text_mensaje.pack(padx=10, pady=(0, 5))
        
        # Frame para botones del área de texto
        text_buttons_frame = tk.Frame(frame, bg="#f0f0f0")
        text_buttons_frame.pack(padx=10, pady=(5, 0))
        
        # Botón de emojis
        btn_emojis = tk.Button(text_buttons_frame, text="😊 Emojis",
                              command=self.abrir_selector_emojis,
                              bg="#ffc107", fg="#212529",
                              font=("Arial", 9, "bold"),
                              width=12, height=1, relief="raised", bd=2)
        btn_emojis.pack(side="left")
        
        # Botón para limpiar texto
        btn_limpiar = tk.Button(text_buttons_frame, text="🗑️ Limpiar",
                               command=lambda: self.text_mensaje.delete("1.0", tk.END),
                               bg="#6c757d", fg="white",
                               font=("Arial", 9),
                               width=12, height=1, relief="raised", bd=2)
        btn_limpiar.pack(side="left", padx=(10, 0))
        
        # Frame para opciones
        opciones_frame = tk.Frame(frame, bg="#f0f0f0")
        opciones_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Checkbox para línea por línea
        tk.Checkbutton(opciones_frame, text="📄 Enviar cada línea como mensaje separado",
                       variable=self.modo_linea_por_linea,
                       font=("Arial", 9), bg="#f0f0f0").pack(anchor="w")

        # Vista previa de caracteres
        self.preview_label = tk.Label(opciones_frame, text="",
                                      font=("Arial", 8), fg="#666666", bg="#f0f0f0")
        self.preview_label.pack(anchor="w", pady=(5, 0))

        # Bind para actualizar preview
        self.text_mensaje.bind('<KeyRelease>', self.actualizar_preview)

    def abrir_selector_emojis(self):
        """Abre una ventana con selector de emojis"""
        emoji_window = tk.Toplevel(self.root)
        emoji_window.title("😊 Selector de Emojis")
        emoji_window.geometry("50x50")
        emoji_window.resizable(True, True)
        emoji_window.configure(bg="#f0f0f0")
        emoji_window.transient(self.root)
        emoji_window.grab_set()

        # Centrar la ventana
        emoji_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 150
        emoji_window.geometry(f"520x900+{x}+{y}")

        # Lista de emojis organizados por categorías
        emojis = {
            "Caras": ["😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊", "😋", "😎", "😍", "😘", "🥰", "😗", "😙", "😚", "🙂", "🤗", "🤔", "😐", "😑", "😶", "🙄", "😏", "😣", "😥", "😮", "🤐", "😯", "😪", "😫", "🥱", "😴", "😌", "😛", "😜", "😝", "🤤"],
            "Gestos": ["👍", "👎", "👌", "🤏", "✌️", "🤞", "🤟", "🤘", "🤙", "👈", "👉", "👆", "🖕", "👇", "☝️", "👋", "🤚", "🖐️", "✋", "🖖", "👏", "🙌", "👐", "🤲", "🤝", "🙏", "✍️", "💪", "🦵", "🦶"],
            "Objetos": ["📱", "💻", "⌨️", "🖥️", "🖨️", "🖱️", "🖲️", "💾", "💿", "📀", "📼", "📷", "📸", "📹", "🎥", "📞", "☎️", "📟", "📠", "📺", "📻", "🎙️", "🎚️", "🎛️", "⏰", "⏲️", "⏱️", "🕰️", "📡", "🔋"],
            "Símbolos": ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝", "💟", "☮️", "✝️", "☪️", "🕉️", "☸️", "✡️", "🔯", "🕎", "☯️", "☦️", "🛐"],
            "Actividad": ["⚽", "🏀", "🏈", "⚾", "🥎", "🎾", "🏐", "🏉", "🎱", "🏓", "🏸", "🏒", "🏑", "🥍", "🏏", "⛳", "🏹", "🎣", "🤿", "🥊", "🥋", "🎽", "⛸️", "🥌", "🛷", "🎿", "⛷️", "🏂", "🏋️", "🤸"],
            "Comida": ["🍎", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦", "🥒", "🥬", "🌶️", "🌽", "🥕", "🥔", "🍠", "🥐", "🍞", "🥖", "🥨", "🧀"]
        }

        # Frame principal con scrollbar
        main_frame = tk.Frame(emoji_window, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(
            main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Función para insertar emoji
        def insertar_emoji(emoji):
            cursor_pos = self.text_mensaje.index(tk.INSERT)
            self.text_mensaje.insert(cursor_pos, emoji)
            self.actualizar_preview()
            emoji_window.destroy()

        # Crear botones de emojis por categoría
        for categoria, lista_emojis in emojis.items():
            # Título de categoría
            titulo_frame = tk.Frame(
                scrollable_frame, bg="#e8f4fd", relief="solid", bd=1)
            titulo_frame.pack(fill="x", pady=(10, 5))
            tk.Label(titulo_frame, text=f"📂 {categoria}", font=("Arial", 10, "bold"),
                    bg="#e8f4fd", fg="#1565c0").pack(pady=5)

            # Frame para los emojis de esta categoría
            emoji_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
            emoji_frame.pack(fill="x", pady=(0, 5))

            # Agregar emojis en filas de 10
            for i, emoji in enumerate(lista_emojis):
                row = i // 10
                col = i % 10

                btn = tk.Button(emoji_frame, text=emoji, font=("Arial", 16),
                                command=lambda e=emoji: insertar_emoji(e),
                                width=3, height=1, relief="flat", bd=1,
                                bg="#ffffff", activebackground="#e3f2fd")
                btn.grid(row=row, column=col, padx=2, pady=2)

        # Instrucciones
        info_frame = tk.Frame(scrollable_frame, bg="#fff3cd", relief="solid", bd=1)
        info_frame.pack(fill="x", pady=10)
        tk.Label(info_frame, text="💡 Haz clic en cualquier emoji para insertarlo en tu mensaje",
                font=("Arial", 9), bg="#fff3cd", fg="#856404").pack(pady=8)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel para scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Limpiar bind cuando se cierre la ventana
        def on_close():
            canvas.unbind_all("<MouseWheel>")
            emoji_window.destroy()

            emoji_window.protocol("WM_DELETE_WINDOW", on_close)

    def create_config_section(self, parent):
        """Sección de configuración"""
        frame = tk.LabelFrame(parent, text="⚙️ CONFIGURACIÓN",
                              font=("Arial", 11, "bold"), bg="#f0f0f0", fg="#2c3e50")
        frame.pack(fill="x", pady=(0, 10))

        # Grid interno
        grid_frame = tk.Frame(frame, bg="#f0f0f0")
        grid_frame.pack(padx=10, pady=10)

        # Fila 1
        tk.Label(grid_frame, text="Cantidad de repeticiones:",
                 font=("Arial", 9), bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=(0, 15))
        self.entry_cantidad = tk.Entry(
            grid_frame, width=8, font=("Arial", 10), justify="center")
        self.entry_cantidad.grid(row=0, column=1, sticky="w")
        self.entry_cantidad.insert(0, "1")

        tk.Label(grid_frame, text="Tiempo de preparación (seg):",
                 font=("Arial", 9), bg="#f0f0f0").grid(row=0, column=2, sticky="w", padx=(30, 15))
        self.entry_delay_inicial = tk.Entry(
            grid_frame, width=8, font=("Arial", 10), justify="center")
        self.entry_delay_inicial.grid(row=0, column=3, sticky="w")
        self.entry_delay_inicial.insert(0, "10")

        # Fila 2
        tk.Label(grid_frame, text="Pausa entre mensajes (seg):",
                 font=("Arial", 9), bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=(0, 15), pady=(10, 0))
        self.entry_delay_entre = tk.Entry(
            grid_frame, width=8, font=("Arial", 10), justify="center")
        self.entry_delay_entre.grid(row=1, column=1, sticky="w", pady=(10, 0))
        self.entry_delay_entre.insert(0, "0.7")

        # Método de envío
        tk.Label(grid_frame, text="Método de envío:",
                 font=("Arial", 9), bg="#f0f0f0").grid(row=1, column=2, sticky="w", padx=(30, 15), pady=(10, 0))

        metodo_frame = tk.Frame(grid_frame, bg="#f0f0f0")
        metodo_frame.grid(row=1, column=3, sticky="w", pady=(10, 0))

        tk.Radiobutton(metodo_frame, text="Portapapeles (Recomendado)",
                       variable=self.metodo_envio, value="portapapeles",
                       font=("Arial", 8), bg="#f0f0f0").pack(anchor="w")

    def create_control_section(self, parent):
        """Sección de control con botones"""
        frame = tk.Frame(parent, bg="#f0f0f0")
        frame.pack(fill="x", pady=(0, 10))

        # Información importante
        info_frame = tk.Frame(frame, bg="#e8f4fd", relief="solid", bd=1)
        info_frame.pack(fill="x", pady=(0, 15))

        info_text = ("💡 INSTRUCCIONES DE USO:\n"
                     "1. Escribe tu mensaje completo (acepta tildes, emojis, caracteres especiales)\n"
                     "2. Ajusta la configuración según tus necesidades\n"
                     "3. Presiona 'INICIAR ENVÍO' y cambia INMEDIATAMENTE a la app objetivo\n"
                     "4. Haz clic en el campo de texto donde quieres enviar los mensajes\n"
                     "5. El script se pausará automáticamente si regresas a esta ventana\n"
                     "🔧 MÉTODO PORTAPAPELES: Más confiable para mensajes largos y caracteres especiales")

        tk.Label(info_frame, text=info_text, font=("Arial", 9),
                 bg="#e8f4fd", fg="#1565c0", justify="left").pack(padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.pack()

        self.btn_iniciar = tk.Button(btn_frame, text="🚀 INICIAR ENVÍO",
                                     command=self.iniciar_envio,
                                     bg="#27ae60", fg="white",
                                     font=("Arial", 10, "bold"),
                                     width=15, height=1, relief="raised", bd=3)
        self.btn_iniciar.pack(side="left", padx=10)

        self.btn_parar = tk.Button(btn_frame, text="⛔ DETENER",
                                   command=self.detener_envio,
                                   bg="#e74c3c", fg="white",
                                   font=("Arial", 10, "bold"),
                                   width=12, height=1, relief="raised", bd=3,
                                   state="disabled")
        self.btn_parar.pack(side="left", padx=10)

        # Botón de test
        self.btn_test = tk.Button(btn_frame, text="🧪 TEST",
                                  command=self.test_mensaje,
                                  bg="#3498db", fg="white",
                                  font=("Arial", 10, "bold"),
                                  width=12, height=1, relief="raised", bd=3)
        self.btn_test.pack(side="left", padx=10)

    def create_status_section(self, parent):
        """Sección de estado y log"""
        frame = tk.LabelFrame(parent, text="📊 ESTADO DEL SISTEMA",
                              font=("Arial", 11, "bold"), bg="#f0f0f0", fg="#2c3e50")
        frame.pack(fill="both", expand=True)

        # Estado actual
        status_frame = tk.Frame(frame, bg="#f0f0f0")
        status_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(status_frame, text="Estado:", font=("Arial", 10, "bold"),
                 bg="#f0f0f0").pack(side="left")
        self.status_label = tk.Label(status_frame, text="💤 En espera",
                                     font=("Arial", 10, "bold"), fg="#27ae60", bg="#f0f0f0")
        self.status_label.pack(side="left", padx=(10, 0))

        # Contador
        self.contador_label = tk.Label(status_frame, text="",
                                       font=("Arial", 10), fg="#7f8c8d", bg="#f0f0f0")
        self.contador_label.pack(side="right")

        # Log
        tk.Label(frame, text="📋 Registro de actividad:", font=("Arial", 9, "bold"),
                 bg="#f0f0f0").pack(anchor="w", padx=10, pady=(0, 5))

        log_frame = tk.Frame(frame, bg="#f0f0f0")
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.text_log = tk.Text(log_frame, height=10, state=tk.DISABLED,
                                bg="#ffffff", font=("Consolas", 9), relief="solid", bd=1)
        scrollbar = tk.Scrollbar(
            log_frame, orient="vertical", command=self.text_log.yview)
        self.text_log.configure(yscrollcommand=scrollbar.set)

        self.text_log.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def actualizar_preview(self, event=None):
        """Actualiza la vista previa del mensaje"""
        try:
            mensaje = self.text_mensaje.get("1.0", tk.END).strip()
            if mensaje:
                chars = len(mensaje)
                lines = len(mensaje.splitlines())
                special_chars = len(re.findall(r'[áéíóúüñÁÉÍÓÚÜÑ¿¡]', mensaje))
                emojis = len(re.findall(r'[🚀📝📤⚙️💡🧪✅❌⏳🛑😅]', mensaje))
                preview_text = f"📊 {chars} caracteres, {lines} líneas"
                if special_chars > 0:
                    preview_text += f", {special_chars} tildes/especiales"
                if emojis > 0:
                    preview_text += f", {emojis} emojis"

                self.preview_label.config(text=preview_text)
            else:
                self.preview_label.config(text="")
        except:
            pass

    def test_mensaje(self):
        """Realiza un test del mensaje sin envío masivo"""
        datos = self.validar_datos()
        if not datos:
            return

        mensaje, _, _, _ = datos

        # Mostrar preview
        lineas = mensaje.splitlines() if self.modo_linea_por_linea.get() else [
            mensaje]
        lineas = [linea.strip() for linea in lineas if linea.strip()]

        preview = "🧪 VISTA PREVIA DEL TEST:\n\n"
        for i, linea in enumerate(lineas[:3]):  # Mostrar máximo 3 líneas
            preview += f"Mensaje {i+1}: {linea[:100]}{'...' if len(linea) > 100 else ''}\n"

        if len(lineas) > 3:
            preview += f"\n... y {len(lineas) - 3} mensaje(s) más"

        preview += f"\n\n📊 Total: {len(lineas)} mensaje(s)"
        preview += f"\n🎯 Método: {self.metodo_envio.get().title()}"

        messagebox.showinfo("🧪 Test de Mensaje", preview)

    def validar_datos(self):
        """Valida los datos ingresados"""
        try:
            mensaje = self.text_mensaje.get("1.0", tk.END).strip()
            cantidad = int(self.entry_cantidad.get())
            delay_inicial = float(self.entry_delay_inicial.get())
            delay_entre = float(self.entry_delay_entre.get())

            if not mensaje:
                raise ValueError("El mensaje no puede estar vacío")
            if cantidad <= 0 or cantidad > 1000:
                raise ValueError("La cantidad debe estar entre 1 y 1000")
            if delay_inicial < 0 or delay_inicial > 120:
                raise ValueError(
                    "El tiempo de preparación debe estar entre 0 y 120 segundos")
            if delay_entre < 0 or delay_entre > 60:
                raise ValueError(
                    "La pausa entre mensajes debe estar entre 0 y 60 segundos")

            return mensaje, cantidad, delay_inicial, delay_entre

        except ValueError as e:
            messagebox.showerror("❌ Error de validación", str(e))
            return None

    def is_window_focused(self):
        """Detecta si nuestra ventana tiene el foco"""
        try:
            return self.root.focus_displayof() is not None and self.root.winfo_viewable()
        except:
            return False

    def enviar_mensaje_portapapeles(self, texto):
        """Envía mensaje usando portapapeles (método más confiable)"""
        try:
            # Guardar contenido actual del portapapeles
            clipboard_original = ""
            try:
                clipboard_original = pyperclip.paste()
            except:
                pass

            # Copiar mensaje al portapapeles
            pyperclip.copy(texto)
            time.sleep(0.1)  # Pequeña pausa para asegurar que se copie

            # Pegar con Ctrl+V
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.05)

            # Enviar con Enter
            pyautogui.press('enter')

            # Restaurar portapapeles original (opcional)
            try:
                if clipboard_original:
                    self.root.after(
                        1000, lambda: pyperclip.copy(clipboard_original))
            except:
                pass

            return True

        except Exception as e:
            self.log(f"❌ Error con portapapeles: {str(e)}")
            return False

    # def enviar_mensaje_typewrite(self, texto):
        """Envía mensaje usando typewrite (método tradicional)"""
        try:
            # Dividir en chunks para textos largos
            chunk_size = 100  # Caracteres por chunk

            if len(texto) <= chunk_size:
                pyautogui.typewrite(texto)
            else:
                # Enviar en chunks para textos largos
                for i in range(0, len(texto), chunk_size):
                    chunk = texto[i:i + chunk_size]
                    pyautogui.typewrite(chunk)
                    time.sleep(0.05)  # Pausa entre chunks

            pyautogui.press('enter')
            return True

        except Exception as e:
            self.log(f"❌ Error con typewrite: {str(e)}")
            return False

    def enviar_mensaje(self, texto):
        """Envía un mensaje usando el método seleccionado"""
        if self.metodo_envio.get() == "portapapeles":
            return self.enviar_mensaje_portapapeles(texto)

    def iniciar_envio(self):
        """Inicia el proceso de envío"""
        if self.enviando:
            return

        datos = self.validar_datos()
        if not datos:
            return

        mensaje, cantidad, delay_inicial, delay_entre = datos

        # Resetear eventos
        self.stop_event.clear()
        self.pause_event.clear()

        # Cambiar estado de la interfaz
        self.enviando = True
        self.btn_iniciar.config(state="disabled")
        self.btn_parar.config(state="normal")
        self.btn_test.config(state="disabled")

        # Iniciar hilo de envío
        self.thread_activo = threading.Thread(
            target=self.proceso_principal,
            args=(mensaje, cantidad, delay_inicial, delay_entre),
            daemon=True
        )
        self.thread_activo.start()

    def proceso_principal(self, mensaje, cantidad, delay_inicial, delay_entre):
        """Proceso principal de envío"""
        try:
            # Fase 1: Countdown inicial
            self.log(f"🕐 Iniciando countdown de {delay_inicial} segundos")
            self.log(
                "📱 Cambia AHORA a la aplicación donde quieres enviar los mensajes")
            self.log(f"🎯 Método de envío: {self.metodo_envio.get().title()}")

            for i in range(int(delay_inicial * 10)):  # Precisión de 0.1 segundos
                if self.stop_event.is_set():
                    return

                remaining = delay_inicial - (i * 0.1)
                self.actualizar_estado(
                    f"⏳ Preparando envío en {remaining:.1f}s")
                time.sleep(0.1)

            # Fase 2: Envío de mensajes
            self.enviar_todos_los_mensajes(mensaje, cantidad, delay_entre)

        except Exception as e:
            self.log(f"❌ Error crítico: {str(e)}")
        finally:
            self.finalizar_envio()

    def enviar_todos_los_mensajes(self, mensaje, cantidad, delay_entre):
        """Envía todos los mensajes con control de pausa"""
        lineas = mensaje.splitlines() if self.modo_linea_por_linea.get() else [
            mensaje]
        lineas = [linea.strip() for linea in lineas if linea.strip()
                  ]  # Filtrar líneas vacías

        total_mensajes = cantidad * len(lineas)
        mensaje_actual = 0

        self.log(f"🚀 Iniciando envío de {total_mensajes} mensaje(s)")
        self.log(
            f"📝 Vista previa: {lineas[0][:50]}{'...' if len(lineas[0]) > 50 else ''}")

        for repeticion in range(cantidad):
            if self.stop_event.is_set():
                break

            for idx_linea, linea in enumerate(lineas):
                if self.stop_event.is_set():
                    break

                # Esperar mientras la ventana esté enfocada
                self.esperar_si_enfocado()

                if self.stop_event.is_set():
                    break

                # Enviar mensaje
                try:
                    exito = self.enviar_mensaje(linea)

                    if exito:
                        mensaje_actual += 1
                        progreso = (mensaje_actual / total_mensajes) * 100

                        # Log del mensaje enviado
                        if len(lineas) > 1:
                            self.log(
                                f"📤 [{progreso:.1f}%] Rep.{repeticion+1} Línea.{idx_linea+1}: {linea[:50]}{'...' if len(linea) > 50 else ''}")
                        else:
                            self.log(
                                f"📤 [{progreso:.1f}%] Mensaje {mensaje_actual}: Enviado correctamente")

                        # Actualizar contador
                        self.contador_label.config(
                            text=f"{mensaje_actual}/{total_mensajes}")
                        self.actualizar_estado(
                            f"📤 Enviando... {progreso:.1f}%")

                        # Pausa entre mensajes
                        if delay_entre > 0 and (mensaje_actual < total_mensajes):
                            time.sleep(delay_entre)
                    else:
                        self.log(
                            f"❌ Error enviando mensaje {mensaje_actual + 1}")
                        break

                except pyautogui.FailSafeException:
                    self.log(
                        "🛑 Envío detenido por FailSafe (mouse en esquina superior izquierda)")
                    return
                except Exception as e:
                    self.log(f"❌ Error crítico enviando mensaje: {str(e)}")
                    break

        if not self.stop_event.is_set():
            self.log("✅ ¡Envío completado exitosamente!")
            self.actualizar_estado("✅ Envío completado")

    def esperar_si_enfocado(self):
        """Espera (pausa) mientras nuestra ventana esté enfocada"""
        pausado = False

        while self.is_window_focused():
            if self.stop_event.is_set():
                return

            if not pausado:
                self.log(
                    "⏸️ PAUSADO - Esta ventana está activa, cambia a la aplicación objetivo")
                self.actualizar_estado(
                    "⏸️ PAUSADO - Cambia de ventana para continuar")
                pausado = True

            time.sleep(0.5)  # Revisa cada 0.5 segundos

        if pausado:
            self.log("▶️ REANUDANDO - Continuando envío...")

    def detener_envio(self):
        """Detiene el envío actual"""
        self.stop_event.set()
        self.log("⛔ Envío detenido por el usuario")

    def finalizar_envio(self):
        """Finaliza el proceso de envío y restaura la interfaz"""
        self.enviando = False
        self.btn_iniciar.config(state="normal")
        self.btn_parar.config(state="disabled")
        self.btn_test.config(state="normal")

        if not self.stop_event.is_set():
            self.actualizar_estado("💤 En espera")
        else:
            self.actualizar_estado("🛑 Detenido")

    def actualizar_estado(self, texto):
        """Actualiza el label de estado de forma thread-safe"""
        try:
            self.root.after(0, lambda: self.status_label.config(text=texto))
        except:
            pass

    def log(self, texto):
        """Añade una entrada al log de forma thread-safe"""
        def _log():
            try:
                timestamp = time.strftime("%H:%M:%S")
                self.text_log.config(state=tk.NORMAL)
                self.text_log.insert(tk.END, f"[{timestamp}] {texto}\n")
                self.text_log.see(tk.END)
                self.text_log.config(state=tk.DISABLED)
            except:
                pass

        self.root.after(0, _log)

    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if self.enviando:
            if messagebox.askokcancel("🚪 Cerrar aplicación",
                                      "Hay un envío en progreso.\n¿Deseas detenerlo y salir?"):
                self.stop_event.set()
                if self.thread_activo and self.thread_activo.is_alive():
                    self.thread_activo.join(timeout=2)
                self.root.destroy()
        else:
            self.root.destroy()

    def run(self):
        """Ejecuta la aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Centrar ventana
        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1000
        window_height = 800

        # Calcular posición central
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Aplicar centrado
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = AutoMensajesPro()
        app.run()
    except KeyboardInterrupt:
        print("\n🛑 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        input("Presiona Enter para salir...")
