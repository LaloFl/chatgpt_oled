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
                                                 
import machine, ssd1306, utime, urequests, network, json

# Conexión con OLED
i2c = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def autoOLEDWrite(text):
    text = text.replace('\xf3', 'o')
    text = text.replace('\xed', 'i')
    text = text.replace('\xe1', 'a')
    text = text.replace('\xe9', 'e')
    text = text.replace('\xfa', 'u')
    text = text.replace('\xf1', 'ni')
    text = text.replace('\xc1', 'A')
    text = text.replace('\xc9', 'E')
    text = text.replace('\xcd', 'I')
    text = text.replace('\xd3', 'O')
    text = text.replace('\xda', 'U')
    text = text.replace('\xd1', 'Ni')
    text = text.replace('\n', '')

    step = 0
    for i in range(len(text)):
        step += 1 if (i % 15 == 0 and i != 0) else 0
        oled.text(text[i], (i%15)*8, step*11)
        # if (i % 15 == 0 and i != 0):
        #     oled.text(text[:((i%15)*step)], 0, step*10)
        #     step += 1

# LED
led = machine.Pin("LED", machine.Pin.OUT)

# Conextión a WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Totalplay-6FA5","paldy969900")

# Wait for connect or fail
while not (wlan.status() < 0 or wlan.status() >= 3):
    print('waiting for connection...')
    oled.fill(0)
    autoOLEDWrite("Waiting for\nConnection")
    oled.show()
    utime.sleep_ms(50)
    led.value(0)
    utime.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    led.value(1)
    ip=wlan.ifconfig()[0]

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
    "Haiku Python",
    "Chiste Python",
    "Dato Python",
    "Dato Radiohead",
]
prompts=[
    "escribe un haiku sobre programación en python",
    "cuenta un chiste sobre programación en python",
    "dime un dato sobre programación en python",
    "dime un dato sobre radiohead",
]

def chatGPT(msg):
    headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
    } 
    payload = {"model": "gpt-3.5-turbo","messages": [{"role": "user","content": msg}]}
    payload = json.dumps(payload).encode("utf-8")
    uri="https://api.openai.com/v1/chat/completions"
    resp = urequests.request("POST", uri, data=payload, headers=headers)

    if resp is not None:
        print(resp.json())
        if resp.status_code != 200:
            print("Error: API request failed with status code", resp.status_code)
        else:
            return resp.json()["choices"][0]["message"]["content"]
    else:
        print("Error: API request failed. No response received.")


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

    # Dibujado de menú
    oled.fill(0)
    oled.text(options[len(options) - 1 if selected - 1 == -1 else selected-1], cols_coords[0]["x"],cols_coords[0]["y"])
    oled.text(options[selected] +" <--", cols_coords[1]["x"] ,cols_coords[1]["y"])
    oled.text(options[(selected+1) % len(options)], cols_coords[2]["x"],cols_coords[2]["y"])
    oled.show()
    
    # Lógica de selección
    if (select == 0):
        oled.fill(0)
        oled.text("Cargando...", 0, 0)
        oled.show()
        # Delay para evitar doble pulsación
        utime.sleep_ms(150)
        msg = str(chatGPT(prompts[selected]))
        oled.fill(0)
        autoOLEDWrite(msg)
        oled.show()
        # Loop de selección
        while True:
            # Lectura de botones
            select_ = btn_select.value()
            up_ = btn_up.value()
            down_ = btn_down.value()
            # Display de selección
            oled.show()
            
            
            
            # Lógica de selección
            oled.scroll(0, -1 if down_ == 0 else 1 if up_ == 0 else 0)
            if (select_ == 0):
                utime.sleep_ms(150)
                break

    # Delay para evitar doble pulsación
    if any([up == 0, down == 0, select == 0]):
        utime.sleep_ms(150)