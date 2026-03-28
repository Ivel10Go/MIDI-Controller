# 🎹 MIDI Controller PCB
 
> A custom MIDI keyboard PCB built as part of the [Hackclub Blueprint](https://blueprint.hackclub.com/starter-projects/midi) program.
 
<img width="1613" height="865" alt="Screenshot 2026-03-28 191607" src="https://github.com/user-attachments/assets/ae14a28e-61ce-43d9-b572-d6b663cfdf7d" />

 
---
 
## Overview
 
This is a fully custom MIDI controller PCB featuring a mechanical switch matrix, per-key RGB lighting, rotary encoders, a high-quality audio DAC, and an ST7735R display — all driven by a Raspberry Pi Pico (Orpheus Pico).
 
<!-- Add more photos here — front/back of PCB, schematic screenshot, 3D render, etc. -->
<!-- ![Schematic](./images/schematic.png) -->
<!-- ![PCB Layout](./images/pcb_layout.png) -->
<img width="1145" height="786" alt="image" src="https://github.com/user-attachments/assets/d3a558a8-a6ca-4bfc-ba94-a8ed5d211313" />
<img width="991" height="683" alt="image" src="https://github.com/user-attachments/assets/eb617484-4a53-4c09-b590-e45821035226" />
<img width="992" height="683" alt="image" src="https://github.com/user-attachments/assets/e4eb08f7-e52e-4a59-8b82-2b3c279fd63e" />



 
---
 
## Features
 
- **38 mechanical keys** in a switch matrix (with 1N4148 diodes for anti-ghosting)
- **38 SK6812MINI-E RGB LEDs** — per-key addressable RGB lighting
- **2 rotary encoders** (Alps EC11E) with clickable push switch
- **PCM5102A audio DAC** with 3.5mm stereo output via I²S
- **ST7735R 1.8" TFT display** via SPI
- **MCP23017 I²C GPIO expander** for the key matrix
- **Raspberry Pi Pico (Orpheus Pico)** as the main microcontroller
- USB powered (5V via Pico)
- M3 and M2.5 mounting holes for case attachment
 
---

##Case

 I decided to go with an open design because I really like the look of the PCB. Thanks to [Miraculix50](https://github.com/Miraculix50) for the help.
 <img width="996" height="529" alt="Screenshot 2026-03-28 200228" src="https://github.com/user-attachments/assets/a702109a-7c59-4dc3-9a00-079f8e2da615" />
<img width="1184" height="420" alt="Screenshot 2026-03-28 200300" src="https://github.com/user-attachments/assets/c7ccae2e-032e-4010-a551-c403f4a26a0e" />


# BOM
Bill of Materials:

Qty. | Item
:-:|:-:
1 | Orpheus Pico
38 | Cherry MX Switch
1 | ST7735R LCD
38 | 1N4148
37 | SK6812 MINI LEDs
1 | XIAO RP2040
2 | EC11 rotary encoders
1 | PCM5100 IIS DAC
1 | MCP23017 I/O Expander
1 | PJ-320A 3.5mm TRRS Audio Jack
2 | 4,7 kΩ
2 | 10 kΩ

