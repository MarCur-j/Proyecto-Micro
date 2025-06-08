import serial

def leer_datos_serial(puerto='COM10', baudios=9600):
    try:
        arduino = serial.Serial(puerto, baudios, timeout=2)
        linea = arduino.readline().decode('utf-8').strip()
        arduino.close()
        return linea
    except Exception as e:
        print(f"Error al leer del puerto serial: {e}")
        return None
