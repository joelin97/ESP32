

from machine import Pin, I2C
import utime, ssd1306, TEA5767
i2c = I2C(scl=Pin(4), sda=Pin(5), freq=400000)
oled=ssd1306.SSD1306_I2C(128,64,i2c)

radio = TEA5767.Radio(i2c, addr=0x60, freq=100.3, band="US", stereo=True,soft_mute=True, noise_cancel=True, high_cut=True)
radio_list = [90.1, 91.7, 92.1, 94.3, 96.3, 98.1, 98.9, 99.7, 100.3, 101.8, 103.3, 104.1, 104.4, 106.5, 107.7]
radio_index = 0
freq = radio_list[radio_index]

rotary_clk = Pin(14, Pin.IN, Pin.PULL_UP)
rotary_dta = Pin(12, Pin.IN, Pin.PULL_UP)
rotary_sw = Pin(13, Pin.IN, Pin.PULL_UP)
led = Pin(16, Pin.OUT)
rotary_clk_prev = rotary_clk

frequency=radio.frequency
oled.text("<< Joe Radio >>"+str(frequency),8,8)
oled.text("FM: "+str(frequency),32,32)
oled.show()
print("ok")
print(rotary_dta)

def update_radio():
    global freq
    if freq < 87.5:
        freq = 87.5
    elif freq > 108.0:
        freq = 108.0
    freq = round(freq, 1)
    #led.off()
    radio.set_frequency(freq=freq)
    oled.fill(0)
    oled.text("Retro FM Radio", 8, 16)

    oled.text("- " + "{:>5}".format(str(round(freq, 1))) + " MHz -", 12, 40)
    oled.show()
    #led.on()

def reset_radio_index():
    global radio_index
    radio_index = 0
    for i in range(len(radio_list) - 1):
        if freq >= radio_list[i] and freq <= radio_list[i + 1]:
            radio_index = i

update_radio()

while True:

    if rotary_sw.value() == 0:
        radio_index += 1
        if radio_index == len(radio_list):
            radio_index = 0
        freq = radio_list[radio_index]
        update_radio()
        utime.sleep_ms(250)

    if rotary_clk_prev == 0 and rotary_clk.value() == 1:
        if rotary_dta.value() == 0:
            freq += 0.1
            reset_radio_index()
            update_radio()
        else:
            freq -= 0.1
            reset_radio_index()
            update_radio()
            
    rotary_clk_prev = rotary_clk.value()
    
    utime.sleep_ms(1)


