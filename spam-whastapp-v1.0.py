import pyautogui
import time
import pyperclip

def enviar_mensajes(mensaje, cantidad, delay_inicial=10):
    print(f"Tienes {delay_inicial} segundos para poner el cursor en la caja de texto...")
    time.sleep(delay_inicial)  # Tiempo para que coloques el cursor donde quieras

    pyperclip.copy(mensaje)  # Copiar el mensaje al portapapeles

    for i in range(cantidad):
        pyautogui.hotkey('ctrl', 'v')  # Pegar el mensaje
        pyautogui.press('enter')       # Presiona Enter para enviar
        print(f"Mensaje {i+1} enviado.")
        time.sleep(0.7)                # Pausa entre mensajes (medio segundo)

if __name__ == "__main__":
    mensaje = input("Escribe el mensaje a enviar: ")
    cantidad = int(input("¿Cuántos mensajes quieres enviar? "))
    delay_inicial = float(input("Segundos para colocar el cursor en el campo de texto (ej: 10): "))

    enviar_mensajes(mensaje, cantidad, delay_inicial)
