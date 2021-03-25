import board
import digitalio
import time
import usb_hid
#import rotaryio
import busio

from adafruit_hid.keyboard import Keyboard

from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from keys_dict.keys import key_lookup

keypress_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP10, board.GP11, board.GP18, board.GP19]
key_pin_array = []

application_id_array =[]

key_codes =[]
keys_pressed =[]

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.DOWN
    key_pin_array.append(key_pin)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

switch_button = digitalio.DigitalInOut(board.GP13)
switch_button.direction = digitalio.Direction.INPUT
switch_button.pull = digitalio.Pull.DOWN

#encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
#last_position = None

uart = busio.UART(tx=board.GP8, rx=board.GP9, baudrate=9600)
uart.write(bytes([0xFF, 0xCD])) #clear screen
uart.write(bytes([0xFF, 0xCC, 0x00, 0x00, 0x00, 0x00]))#set origin ot 0,0


#open shortcuts.txt file and put contents in application_dict so title and shortcut can be looked up for each application
application_dict={}
with open("/shortcuts.txt","r") as fp:
    for line in fp:
        app,desc,keys=line.split(",")
        combo=[]
        for key in keys.split():
            combo.append(key_lookup[key])
        if app in application_dict:
            application_dict[app].append((desc.strip(),combo))
        else:
            application_dict[app]=[(desc.strip(),combo)]

#if desktop is a set of shortcuts in the file then start with desktop as the default
if "Desktop" in application_dict.keys():
    application_id = "Desktop"
else:
    application_id = list(application_dict.keys())[0]

#put info on the LCD screen, name of each shortcut in a grid that corresponds to the keys and the application the shortcuts are for
def draw_display(application_id):
    uart.write(bytes([0xFF, 0xCD])) #clear screen

    uart.write(bytes([0xFF, 0xC4, 0x00, 0x00, 0x00,0x00, 0x00, 0xEF, 0x00, 0x3B, 0x00, 0x00])) #draw solid rectangle for top
    #draw grid of buttons
    uart.write(bytes([0xFF, 0xC4, 0x00, 0x00, 0x00,0x3C, 0x00, 0xEF, 0x00, 0xEF, 0x84, 0x10]))
    #           FFC5:rec outline   start x     start y     end x        end y      colour
    #draw lines for seperating buttons
    uart.write(bytes([0xFF, 0xC8, 0x00, 0x00, 0x00, 0x78, 0x00, 0xEF, 0x00, 0x78, 0x00, 0x00]))
    uart.write(bytes([0xFF, 0xC8, 0x00, 0x00, 0x00, 0xB4, 0x00, 0xEF, 0x00, 0xB4, 0x00, 0x00]))

    uart.write(bytes([0xFF, 0xC8, 0x00, 0x3C, 0x00, 0x3C, 0x00, 0x3C, 0x00, 0xEF, 0x00, 0x00]))
    uart.write(bytes([0xFF, 0xC8, 0x00, 0x78, 0x00, 0x3C, 0x00, 0x78, 0x00, 0xEF, 0x00, 0x00]))
    uart.write(bytes([0xFF, 0xC8, 0x00, 0xB4, 0x00, 0x3C, 0x00, 0xB4, 0x00, 0xEF, 0x00, 0x00]))

    uart.write(bytes([0xFF, 0xE7, 0xFF, 0xFF]))#forground/text colour white
    uart.write(bytes([0xFF, 0xE6, 0x00, 0x00]))#background colour black

    uart.write(bytes([0xFF, 0xE5, 0x00, 0x02])) #set font 3
    uart.write(bytes([0xFF, 0xE4, 0x00, 0x02])) #double text width
    uart.write(bytes([0xFF, 0xE3, 0x00, 0x02])) #double text height

    #move origin so header in middle for shortcut application name
    header_len = len(application_id)
    spacing = (240-(header_len*(8*2)))//2
    spacing_height = (60-(12*2))//2
    uart.write(bytes([0xFF, 0xCC, 0x00, spacing, 0x00, spacing_height])) #move origin
    uart.write(bytes([0x00, 0x18]))
    uart.write(application_id.encode('ascii'))
    uart.write(bytes([0x00]))

    uart.write(bytes([0xFF, 0xE5, 0x00, 0x02])) #set font 3
    uart.write(bytes([0xFF, 0xE4, 0x00, 0x01])) #normal text width
    uart.write(bytes([0xFF, 0xE3, 0x00, 0x01])) #normal text height


    #fill in grid with shortcut names
    uart.write(bytes([0xFF, 0xE7, 0xFF, 0xFF]))#forground/text colour white
    uart.write(bytes([0xFF, 0xE6, 0x84, 0x10]))#background colour grey
    short_num=0
    for iy in range(3):
        grid_y = 60 + (iy*60)+1

        for ix in range(4):
            grid_x = (ix*60)+1
            text_to_print = (application_dict[application_id][short_num][0]).split(" ")
            if (len(text_to_print))==1:
                label_x = grid_x+((60-(len(text_to_print[0]))*8)//2)
                label_y = grid_y+((60-12)//2)
                uart.write(bytes([0xFF, 0xCC, 0x00, label_x, 0x00, label_y])) #move origin
                uart.write(bytes([0x00, 0x18]))
                uart.write(text_to_print[0].encode('ascii'))
                uart.write(bytes([0x00]))
            elif (len(text_to_print))==2:
                label_x = grid_x+((60-len(text_to_print[0])*8)//2)
                label_y = grid_y+((60-(12*2))//2)-2
                uart.write(bytes([0xFF, 0xCC, 0x00, label_x, 0x00, label_y])) #move origin
                uart.write(bytes([0x00, 0x18]))
                uart.write(text_to_print[0].encode('ascii'))
                uart.write(bytes([0x00]))
                label_x = grid_x+((60-len(text_to_print[1])*8)//2)
                label_y = label_y + 12 +2
                uart.write(bytes([0xFF, 0xCC, 0x00, label_x, 0x00, label_y])) #move origin
                uart.write(bytes([0x00, 0x18]))
                uart.write(text_to_print[1].encode('ascii'))
                uart.write(bytes([0x00]))
            else:
                label_x = grid_x+((60-len(text_to_print[0])*8)//2)
                label_y = grid_y+((60-(12*3))//2)-6
                uart.write(bytes([0xFF, 0xCC, 0x00, label_x, 0x00, label_y])) #move origin
                uart.write(bytes([0x00, 0x18]))
                uart.write(text_to_print[0].encode('ascii'))
                uart.write(bytes([0x00]))
                label_x = grid_x+((60-len(text_to_print[1])*8)//2)
                label_y = label_y + 12 +2
                uart.write(bytes([0xFF, 0xCC, 0x00, label_x, 0x00, label_y])) #move origin
                uart.write(bytes([0x00, 0x18]))
                uart.write(text_to_print[1].encode('ascii'))
                uart.write(bytes([0x00]))
                label_x = grid_x+((60-len(text_to_print[2])*8)//2)
                label_y = label_y + 12 +2
                uart.write(bytes([0xFF, 0xCC, 0x00, label_x, 0x00, label_y])) #move origin
                uart.write(bytes([0x00, 0x18]))
                uart.write(text_to_print[2].encode('ascii'))
                uart.write(bytes([0x00]))

            short_num=short_num+1


draw_display(application_id)
while True:
    #encoder temporary commented out, rotaryio currently not working in circuitpython 6.2.0-beta3, using the press button on rotary encoder instead
    #position = encoder.position
    #if last_position is None or position != last_position:
    #    print(position)
    #last_position = position

    #if rotary encoder button is pressed then change application shortcuts displayed to the next application and redraw the display
    if switch_button.value:
        while switch_button.value:
            pass
        idx = list(application_dict.keys()).index(application_id)
        application_id = list(application_dict.keys())[(idx+1)%len(list(application_dict.keys()))]
        print(application_id)
        draw_display(application_id)

    for key_pin in key_pin_array:
        if key_pin.value:
            i = key_pin_array.index(key_pin)
            led.value = True
            while key_pin.value:
                pass
                #on key press release continue ot look up shortcut keypress required and press it.
            key = application_dict[application_id][i][1]

            keyboard.press(*key)
            keyboard.release_all()

            led.value = False
    time.sleep(0.01)