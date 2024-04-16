from pyautogui import *
import pyautogui
import time
import datetime
import random
import win32api
import win32con
import sys
import tkinter as tk
from tkinter import IntVar, ttk
import threading
import keyboard


# Crea una instancia de Tkinter
root = tk.Tk()

# Estado de pausa
pause_flag = False
stop_flag = False

timeout = 5 # Si el programa se bloquea durante 5 segundos, terminar
debug_timer = 0 #Para hacer pruebas poner en 2, hara que despues del scroll espere 2 segundos para dar tiempo a comprobar
exit_flag = 0
run_timeout = 0

rand_x = random.randrange(-60, 60)
rand_y = random.randrange(-15, 15)

# Define una función para pausar o reanudar la ejecución de la macro
def pause_resume_macro():
    global pause_flag
    pause_flag = not pause_flag

# Define una función para pausar la ejecución de la macro
def pause_macro():
    global pause_flag
    pause_flag = not pause_flag

def stop_macro(event=None):
    global stop_flag
    stop_flag = not stop_flag

# Define una función para ejecutar la macro en segundo plano
def run_macro():
    global run_timeout, stop_flag
    stop_flag = False
    macro_thread = threading.Thread(target=macro)
    macro_thread.start()

def on_closing():
    global exit_flag
    exit_flag = 1
    time.sleep(1)
    sys.exit()

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.4)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def chk_dispatch():
    pos = pyautogui.locateOnScreen('my_images/dispatch_confirm.png', confidence=0.8)
    if pos is not None:
        time.sleep(1)
        pos_center = pyautogui.center(pos)
        click(pos_center.x + rand_x, pos_center.y + rand_y)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.4)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def locateAndClick(imgName):
    time.sleep(0.8)
    image = pyautogui.locateOnScreen('my_images/' + imgName +'.png', confidence=0.8)
    if image is None:
        print("Error: Boton de " + imgName + " no encontrado.")
        sys.exit()
    # Click image
    RB_center = pyautogui.center(image)
    click(RB_center[0], RB_center[1])
    time.sleep(0.8)

def refill():
    time.sleep(0.4)
    image = pyautogui.locateOnScreen('my_images/refill.png', confidence=0.8)
    if image is not None:
        locateAndClick("refill")
        time.sleep(0.8)
        locateAndClick("start")

def macro():
    global exit_flag, debug_timer, macro_thread, stop_flag

    macro_thread = threading.current_thread()

    while exit_flag == 0 and not stop_flag:
        if not pause_flag:

            time.sleep(0.3)
            chk_dispatch()

            image = pyautogui.locateOnScreen('my_images/w13-confirm.png', confidence=0.8)
            while image is None and not stop_flag:
                time.sleep(2)
                image = pyautogui.locateOnScreen('my_images/stopedRun.png', confidence=0.8)

            # Localizar botón de mochila
            locateAndClick("bag")

            # Localizar botón de mochila
            locateAndClick("sort")

            # Seleccionar gear aut.
            locateAndClick("auto-select-gear-sencillo")

            # Seleccionar vender o extraer
            locateAndClick("extract")
            locateAndClick("extract-part2")

            # Click en confirmar para cerrar ventana de mochila
            locateAndClick("w13-confirm")

            # Click en confirmar
            locateAndClick("w13-confirm")

            # Localizar botón de retry
            locateAndClick("retry")

            # Localizar botón de start
            locateAndClick("start")
            refill()


# Configurar el tamaño y título de la ventana
root.geometry("200x50")
root.title("Epic Seven Macro")

# Configurar la ventana para que esté siempre en primer plano
root.wm_attributes("-topmost", 1)

# Crear un estilo base
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

# Crear un contenedor para el campo de entrada y el botón
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Crear un botón para ejecutar la macro
button_run_macro = ttk.Button(frame, text="Iniciar", command=run_macro)
button_run_macro.grid(row=0, column=1, rowspan=2, padx=10, pady=(0, 5), sticky="NS")

# Enlazar la pulsación de tecla de Escape para detener la macro
keyboard.on_press_key("esc", stop_macro, suppress=True)

root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar el bucle principal de la interfaz de usuario
root.mainloop()