# nfc_antenna_generator
Generate an NFC antenna module for kicad.

## Howto
Call `python3 antGen.py -h` from your terminal to see how to use the script or overwrite the constants in antGen.py and then call the script without any arguments `python3 antGen.py`. The generated module will be written to `./nfc_ant.pretty/`.

### Terms
The used terms / dimensions are shown here (note: minimalConductorSpace is only needed when style 2 is chosen):
![style 1](https://raw.githubusercontent.com/nideri/nfc_antenna_generator/master/doc/ant_dimensions.png)

## Calculate antenna inductance
The whole project is inspired by the eDesign Antenna tool from ST. Go to https://my.st.com/analogsimulator/html_app/antenna/#/ to design your antenna and use these values to generate an corresponding antenna module for kicad with antGen.py.

## Tested
I only tested it on my machine with Python 3.7.3 and kicad Version: 5.0.2+dfsg1-1, release build, Platform: Linux 4.19.0-6-amd64 x86_64 

## Styles
Three styles are availabe:

### Style 1
![style 1](https://raw.githubusercontent.com/nideri/nfc_antenna_generator/master/doc/ant_style_1.png)

### Style 2
![style 2](https://raw.githubusercontent.com/nideri/nfc_antenna_generator/master/doc/ant_style_2.png)

### Style 3
![style 3](https://raw.githubusercontent.com/nideri/nfc_antenna_generator/master/doc/ant_style_3.png)
