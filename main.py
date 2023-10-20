# Código por Diego Eduardo Flores Sandoval
# https://github.com/LaloFl                         
                                                   
#                        ,,                      ,,  
# `7MMF'               `7MM         `7MM"""YMM `7MM  
#   MM                   MM           MM    `7   MM  
#   MM         ,6"Yb.    MM  ,pW"Wq.  MM   d     MM  
#   MM        8)   MM    MM 6W'   `Wb MM""MM     MM  
#   MM      ,  ,pm9MM    MM 8M     M8 MM   Y     MM  
#   MM     ,M 8M   MM    MM YA.   ,A9 MM         MM  
# .JMMmmmmMMM `Moo9^Yo..JMML.`Ybmd9'.JMML.     .JMML.
                                                 
import machine, ssd1306, utime

# Conexión con OLED
i2c = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Conexión con botones
btn_select = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
btn_up = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
btn_down = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)

# Coordenadas de las columnas
cols_coords = [
    {"x":0,"y":0},
    {"x":0,"y":28},
    {"x":0,"y":56},
]

# Opciones del menú
options=[
    "Option #1",
    "Option #2",
    "Option #3",
    "Option #4",
    "Option #5",
    "Option #6",
]

# Loop principal
selected=0
while True:
    # Lectura de botones
    select = btn_select.value()
    up = btn_up.value()
    down = btn_down.value()

    # Lógica de selección
    try:
        selected = (selected + (1 if down == 0 else -1 if up == 0 else len(options)-1 if up == 0 and selected == 0 else 0)) % len(options)
    except:
        pass
    
    # Delay para evitar doble pulsación
    if any([up == 0, down == 0, select == 0]):
        utime.sleep_ms(150)

    # Dibujado de menú
    oled.fill(0)
    oled.text(options[len(options) - 1 if selected - 1 == -1 else selected-1], cols_coords[0]["x"],cols_coords[0]["y"])
    oled.text(options[selected] +" <--", cols_coords[1]["x"] ,cols_coords[1]["y"])
    oled.text(options[(selected+1) % len(options)], cols_coords[2]["x"],cols_coords[2]["y"])
    oled.show()
    
    # Lógica de selección
    if (select == 0):
        # Delay para evitar doble pulsación
        utime.sleep_ms(150)
        # Loop de selección
        while True:
            # Display de selección
            oled.fill(0)
            oled.text("Selected: ", 0,0)
            oled.text(options[selected], 30,30)
            oled.show()
            # Lectura de botón de selección
            if (btn_select.value() == 0):
                utime.sleep_ms(150)
                break
