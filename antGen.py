#!/bin/env python3
#
# ---------------------------------------------------------------------------
#    N F C   A N T E N N A   G E N E R A T O R
# ---------------------------------------------------------------------------
#
# 2019-11-15 by mui
#
# usage: ./antGen.py -h
#
# output will be written to ./nfc_ant.pretty/
#
# to calculate antenna inductance, check https://my.st.com/analogsimulator/html_app/antenna/#/
#
# tested with Python 3.7.3 and kicad Version: 5.0.2+dfsg1-1, release build, Platform: Linux 4.19.0-6-amd64 x86_64
#
# WARNING: There will be a "Pad near pad" Error when you do the DRC in pcbnew. 
#          This occures from the fact, that you have to connect to pads together (shorten) when you design a current antenna.
#          I have no clean way to suppress this Error. I could use a polygon to draw coil but then it's possible to cross with traces. I don't like that either... Do you have an idea?
#
# ---------------------------------------------------------------------------
#   if script is started with no arguments, this block of constants will be taken
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
c_modulename              = 'nfc_ant' # [-]   - generated module will be saved under nfc_ant.pretty/<modulename>.kicad_mod
c_turns                   = 3         # [#]   - number of windings, see doc/st.png
c_antennaLength           = 75.4      # [mm]  - lenght of antenna (copper outer copper dimension), compare with doc/st.png
c_antennaWidth            = 33.5      # [mm]  - width of antenna (outer copper dimension), compare with doc/st.png
c_conductorWidth          = 2.7       # [mm]  - width of conductor, compare with doc/st.png
c_conductorSpace          = 1.7       # [mm]  - width of space between conductors, compare with doc/st.png
c_drillSize               = -1        # [mm]  - drill size for pad holes in mm (diameter). if set to 0, pads will be smd instead of tht. if set to value < 0, drillSize is set to floor(conductorWidth/2*10)/10
c_minimalConductorSpace   = -1        # [mm]  - needed only for style=2, describes space between conductors on slope. when set to a negative value, minimalConductorSpace will be set to conductorSpace/sqrt(2)
c_silkMargin              = 1.0       # [mm]  - margin of silkscreen outline to outer copper. if set to value < 0, no outline will be drawn   
c_style                   = 3         # [#]   - how should the antenna look like
                                      #           1) see doc/ant_style_1.png
                                      #           2) see doc/ant_style_2.png
                                      #           3) see doc/ant_style_3.png
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SKRIPT_VERSION="1.1"

import math

def genAnt( turns,          # [#]   
            antLength,      # [mm]  
            antWidth,       # [mm]  
            condWidth,      # [mm]  
            condSpace,      # [mm]
            drillSize,      # [mm]
            condSpaceMin,   # [mm]
            silkMargin,     # [mm]
            name,           # [-]
            style           # [-]
      ):

    # https://stackoverflow.com/questions/7852855/in-python-how-do-you-convert-a-datetime-object-to-seconds#30156392
    from datetime import datetime
    dt = datetime.today()  # Get timezone naive now
    seconds = int(dt.timestamp())

    if drillSize < 0:
        drillSize = math.floor(condWidth/2*10)/10
        if drillSize == 0:
            print("WARNING: drillSize was < 0 and is therefore autocalculated. the resulted drillSize is 0! tht pad is replaced by smd pad. select drillSize manually!")
    if drillSize > condWidth:
        print("WARNING: drillSize > conductorWidth!")

    mod=""
    mod="%s(module %s (layer F.Cu) (tedit %X)\n" % (mod, name, seconds)
    mod="%s  (fp_text reference REF** (at %f %f) (layer F.SilkS)\n" % (mod, antLength/2, antWidth/2)
    mod="%s    (effects (font (size 1 1) (thickness 0.15)))\n" % (mod)
    mod="%s  )\n" % (mod)
    mod="%s  (fp_text value %s (at %f %f) (layer F.Fab)\n" % (mod, name, antLength/2, antWidth/2+2)
    mod="%s    (effects (font (size 1 1) (thickness 0.15)))\n" % (mod)
    mod="%s  )\n" % (mod)
    if silkMargin >= 0:
        # show outline on top silk
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.15))\n" % (mod, -silkMargin, -silkMargin, antLength+silkMargin, -silkMargin)  # t
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.15))\n" % (mod, antLength+silkMargin, -silkMargin, antLength+silkMargin, antWidth+silkMargin)  # r
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.15))\n" % (mod, antLength+silkMargin, antWidth+silkMargin, -silkMargin, antWidth+silkMargin) # b
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.15))\n" % (mod, -silkMargin, antWidth+silkMargin, -silkMargin, -silkMargin) # l
        # mark only corners on bottom silk
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer B.SilkS) (width 0.15))\n" % (mod, -silkMargin, -silkMargin, (turns*(condWidth+condSpace)-condSpace+silkMargin), -silkMargin) # tl -> right
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer B.SilkS) (width 0.15))\n" % (mod, -silkMargin, -silkMargin, -silkMargin, (turns*(condWidth+condSpace)-condSpace+silkMargin)) # tl -> down 
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer B.SilkS) (width 0.15))\n" % (mod, antLength+silkMargin, -silkMargin, antLength-(turns*(condWidth+condSpace)-condSpace+silkMargin), -silkMargin) # tr -> left
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer B.SilkS) (width 0.15))\n" % (mod, antLength+silkMargin, -silkMargin, antLength+silkMargin, (turns*(condWidth+condSpace)-condSpace+silkMargin))  # tr -> down 
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer B.SilkS) (width 0.15))\n" % (mod, antLength+silkMargin, antWidth+silkMargin, antLength-(turns*(condWidth+condSpace)-condSpace+silkMargin), antWidth+silkMargin) # br -> left
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer B.SilkS) (width 0.15))\n" % (mod, antLength+silkMargin, antWidth+silkMargin, antLength+silkMargin, antWidth-(turns*(condWidth+condSpace)-condSpace+silkMargin)) # br -> up 
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer B.SilkS) (width 0.15))\n" % (mod, -silkMargin, antWidth+silkMargin, (turns*(condWidth+condSpace)-condSpace+silkMargin), antWidth+silkMargin)  # bl -> right
        mod="%s  (fp_line (start %f %f) (end %f %f) (layer B.SilkS) (width 0.15))\n" % (mod, -silkMargin, antWidth+silkMargin, -silkMargin, antWidth-(turns*(condWidth+condSpace)-condSpace+silkMargin)) # bl -> up 
    # draw antenna
    if style == 3: # const 45 deg slope
        xg=((math.sqrt(2)-1)*turns+1)*(condWidth+condSpace)
        yg=(turns-1)*(condWidth+condSpace)
        dx1=(math.sqrt(2)-1)*(condWidth+condSpace)
        dx2=(condWidth+condSpace)*math.sqrt(2)
        dy=(condWidth+condSpace)
        if drillSize > 0:
            mod="%s  (pad 1 thru_hole circle (at %f %f) (size %f %f) (drill %f) (layers *.Cu *.Mask))\n" % (mod, antLength/2-xg/2, antWidth-condWidth/2, condWidth, condWidth, drillSize)
        mod="%s  (pad 1 smd custom (at %f %f) (size %f %f) (layers F.Cu)\n" % (mod, antLength/2-xg/2, antWidth-condWidth/2, condWidth, condWidth)
        mod="%s    (zone_connect 0)\n" % (mod)
        mod="%s    (options (clearance outline) (anchor circle))\n" % (mod)
        mod="%s    (primitives\n" % (mod)
        x0 = 0
        y0 = 0
        seg = 0
        d = 0
        for seg in range(0,turns*6-2):
            if seg%6 == 0: # line goes left from middle
                x1 = x0 - (antLength/2-xg/2-condWidth/2-d) - int(seg/6)*dx1
                y1 = y0
            elif seg%6 == 1: # line goes up
                x1 = x0 
                y1 = y0 - (antWidth-condWidth-2*d)
            elif seg%6 == 2: # line right
                x1 = x0 + (antLength-condWidth-2*d)
                y1 = y0
            elif seg%6 == 3: # line down
                x1 = x0
                y1 = y0 + (antWidth-condWidth-2*d)
            elif seg%6 == 4: # line goes left to the middle
                x1 = x0 - (antLength/2-xg/2-condWidth/2-d) - (turns-1-int(seg/6))*dx1
                y1 = y0
            elif seg%6 == 5: # line from the middle with a slope to the next level
                x1 = x0 - dx2 + dx1
                y1 = y0 - dy
                d = d + condSpace + condWidth
            mod="%s      (gr_line (start %f   %f) (end %f %f) (width %f))\n" % (mod, x0, y0, x1, y1, condWidth)
            x0 = x1
            y0 = y1
        mod="%s    ))\n" % (mod)
        if drillSize > 0:
            mod="%s  (pad 2 thru_hole circle (at %f %f) (size %f %f) (drill %f) (layers *.Cu *.Mask))\n" % (mod, antLength/2+xg/2, antWidth-condWidth/2-yg, condWidth, condWidth, drillSize)
        mod="%s  (pad 2 smd custom (at %f %f) (size %f %f) (layers F.Cu)\n" % (mod, antLength/2+xg/2, antWidth-condWidth/2-yg, condWidth, condWidth)
        mod="%s    (zone_connect 0)\n" % (mod)
        mod="%s    (options (clearance outline) (anchor circle))\n" % (mod)
        mod="%s    (primitives\n" % (mod)
        mod="%s      (gr_line (start %f   %f) (end %f %f) (width %f))\n" % (mod, 0, 0,  (antLength/2-xg/2-condWidth/2-d) + (turns-1-int(seg/6))*dx1, 0, condWidth)
        mod="%s    ))\n" % (mod)
    elif style == 2: # slope always on the same x location
        if condSpaceMin<0:
            condSpaceMin=condSpace/math.sqrt(2)
        alpha=math.asin((condWidth+condSpaceMin)/(condWidth+condSpace))
        yg=condWidth+condSpace
        xg=math.tan(alpha)*yg
        if drillSize > 0:
            mod="%s  (pad 1 thru_hole circle (at %f %f) (size %f %f) (drill %f) (layers *.Cu *.Mask))\n" % (mod, antLength/2-xg/2, antWidth-condWidth/2, condWidth, condWidth, drillSize)
        mod="%s  (pad 1 smd custom (at %f %f) (size %f %f) (layers F.Cu)\n" % (mod, antLength/2-xg/2, antWidth-condWidth/2, condWidth, condWidth)
        mod="%s    (zone_connect 0)\n" % (mod)
        mod="%s    (options (clearance outline) (anchor circle))\n" % (mod)
        mod="%s    (primitives\n" % (mod)
        x0 = 0
        y0 = 0
        seg = 0
        d = 0
        for seg in range(0,turns*6-2):
            if seg%6 == 0: # line goes left from middle
                x1 = x0 - (antLength/2-xg/2-condWidth/2-d)
                y1 = y0
            elif seg%6 == 1: # line goes up
                x1 = x0 
                y1 = y0 - (antWidth-condWidth-2*d)
            elif seg%6 == 2: # line right
                x1 = x0 + (antLength-condWidth-2*d)
                y1 = y0
            elif seg%6 == 3: # line down
                x1 = x0
                y1 = y0 + (antWidth-condWidth-2*d)
            elif seg%6 == 4: # line goes left to the middle
                x1 = x0 - (antLength/2-xg/2-condWidth/2-d)
                y1 = y0
            elif seg%6 == 5: # line from the middle with a slope to the next level
                x1 = x0 - xg
                y1 = y0 - yg
                d = d + condSpace + condWidth
            mod="%s      (gr_line (start %f   %f) (end %f %f) (width %f))\n" % (mod, x0, y0, x1, y1, condWidth)
            x0 = x1
            y0 = y1
        mod="%s    ))\n" % (mod)
        if drillSize > 0:
            mod="%s  (pad 2 thru_hole circle (at %f %f) (size %f %f) (drill %f) (layers *.Cu *.Mask))\n" % (mod, antLength/2-xg/2+xg, antWidth-condWidth/2+y0, condWidth, condWidth, drillSize)
        mod="%s  (pad 2 smd custom (at %f %f) (size %f %f) (layers F.Cu)\n" % (mod, antLength/2-xg/2+xg, antWidth-condWidth/2+y0, condWidth, condWidth)
        mod="%s    (zone_connect 0)\n" % (mod)
        mod="%s    (options (clearance outline) (anchor circle))\n" % (mod)
        mod="%s    (primitives\n" % (mod)
        mod="%s      (gr_line (start %f   %f) (end %f %f) (width %f))\n" % (mod, 0, 0,  antLength/2-xg/2-condWidth/2 - (turns-1)*(condWidth+condSpace), 0, condWidth)
        mod="%s    ))\n" % (mod)
    else: # simple, with no slope, pads in corner
        if drillSize > 0:
          mod="%s  (pad 1 thru_hole circle (at %f %f) (size %f %f) (drill %f) (layers *.Cu *.Mask))\n" % (mod, condWidth/2, antWidth-condWidth/2, condWidth, condWidth, drillSize)
        mod="%s  (pad 1 smd custom (at %f %f) (size %f %f) (layers F.Cu)\n" % (mod, condWidth/2, antWidth-condWidth/2, condWidth, condWidth)
        mod="%s    (zone_connect 0)\n" % (mod)
        mod="%s    (options (clearance outline) (anchor circle))\n" % (mod)
        mod="%s    (primitives\n" % (mod)
        x0 = 0
        y0 = 0
        seg = 0
        dx = antLength-condWidth
        dy = antWidth-condWidth
        for seg in range(0,turns*4-1):
            if seg%4 == 0: # line goes up
                x1 = x0
                y1 = y0 - dy
            elif seg%4 == 1: # line goes right
                if int(seg/4) > 0: # not for 1st right
                    dx = dx - condWidth-condSpace
                x1 = x0 + dx
                y1 = y0
            elif seg%4 == 2: # line goes down
                if int(seg/4) > 0: # not for 1st down
                    dy = dy - condWidth-condSpace
                x1 = x0
                y1 = y0 + dy
            elif seg%4 == 3: # line goes left
                dx = dx - condWidth - condSpace
                x1 = x0 - dx
                y1 = y0
                dy = dy - condWidth - condSpace
            mod="%s      (gr_line (start %f   %f) (end %f %f) (width %f))\n" % (mod, x0, y0, x1, y1, condWidth)
            x0 = x1
            y0 = y1
        mod="%s    ))\n" % (mod)
        if drillSize > 0:
            mod="%s  (pad 2 thru_hole circle (at %f %f) (size %f %f) (drill %f) (layers *.Cu *.Mask))\n" % (mod, condWidth/2+turns*(condWidth+condSpace), antWidth-condWidth/2+y0, condWidth, condWidth, drillSize)
        mod="%s  (pad 2 smd custom (at %f %f) (size %f %f) (layers F.Cu)\n" % (mod, condWidth/2+turns*(condWidth+condSpace), antWidth-condWidth/2+y0, condWidth, condWidth)
        mod="%s    (zone_connect 0)\n" % (mod)
        mod="%s    (options (clearance outline) (anchor circle))\n" % (mod)
        mod="%s    (primitives\n" % (mod)
        mod="%s      (gr_line (start %f   %f) (end %f %f) (width %f))\n" % (mod, 0, 0,  antLength + condSpace - 2*turns*(condWidth+condSpace), 0, condWidth)
        mod="%s    ))\n" % (mod)
        
    mod="%s)\n" % (mod)
    return mod

# -----------------------------------------------------------------------------
#    M A I N
# -----------------------------------------------------------------------------

import sys, argparse, os

def main(args):
   
    # called with arguments?
    if len(args) > 0:
        parser=argparse.ArgumentParser()
        parser.add_argument("-f", "--modulename"           ,                         help="generated module will be saved under nfc_ant.pretty/<modulename>.kicad_mod", required=True)
        parser.add_argument("-n", "--turns"                , type=int,               help="number of windigs, see doc/st.png", required=True)
        parser.add_argument("-l", "--antennaLength"        , type=float,             help="lenght of antenna in mm (outer copper dimension), compare with doc/st.png", required=True)
        parser.add_argument("-w", "--antennaWidth"         , type=float,             help="width of antenna in mm (outer copper dimension), compare with doc/st.png", required=True)
        parser.add_argument("-c", "--conductorWidth"       , type=float,             help="width of conductor in mm, compare with doc/st.png", required=True)
        parser.add_argument("-s", "--conductorSpace"       , type=float,             help="width of space between conductors in mm, compare with doc/st.png", required=True)
        parser.add_argument("-d", "--drillSize"            , type=float,             help="drill size for pad holes in mm (diameter). if set to 0, pads will be smd, not tht. if set to value < 0, drillSize is set to floor(conductorWidth/2*10)/10", required=False)
        parser.add_argument("-e", "--minimalConductorSpace", type=float, default=-1, help="used only when style=2, describes space between conductors on slope in mm. will be set to -1 if not provided. when set to a negative value, minimalConductorSpace will be set to conductorSpace/sqrt(2)", required=False)
        parser.add_argument("-m", "--silkMargin"           , type=float, default=0 , help="margin of silkscreen outline to outer copper in mm, will be set to 0 if not provided. if set to value < 0, no outline will be drawn", required=False)
        parser.add_argument("-t", "--style"                , type=int  , default=1 , help="how should the antenna look like, will be set to 1 if not provided. 1: see doc/st.png or doc/ant_style_1.png | 2: see doc/ant_style_2.png | 3: see doc/ant_style_3.png", required=False, choices=[1,2,3])

        args=parser.parse_args()

        # overwrite constants from above
        modulename            = args.modulename          
        turns                 = args.turns
        antennaLength         = args.antennaLength        
        antennaWidth          = args.antennaWidth         
        conductorWidth        = args.conductorWidth       
        conductorSpace        = args.conductorSpace      
        drillSize             = args.drillSize
        minimalConductorSpace = args.minimalConductorSpace
        silkMargin            = args.silkMargin           
        style                 = args.style              
    else:        
        # take constants from top when script is called without any arguments
        modulename              = c_modulename           
        turns                   = c_turns                
        antennaLength           = c_antennaLength        
        antennaWidth            = c_antennaWidth         
        conductorWidth          = c_conductorWidth       
        conductorSpace          = c_conductorSpace       
        drillSize               = c_drillSize            
        minimalConductorSpace   = c_minimalConductorSpace
        silkMargin              = c_silkMargin             
        style                   = c_style                
    
    # generate antenna
    ant=genAnt( turns=turns,                        # [#]   
                antLength=antennaLength,            # [mm]  
                antWidth=antennaWidth,              # [mm]  
                condWidth=conductorWidth,           # [mm]  
                condSpace=conductorSpace,           # [mm]
                drillSize=drillSize,                # [mm]
                condSpaceMin=minimalConductorSpace, # [mm]
                silkMargin=silkMargin,              # [mm]
                name=modulename,                    # [-]
                style=style)                        # [-]

    # write result to file
    if not os.path.exists('./nfc_ant.pretty'):
        os.makedirs('./nfc_ant.pretty')
    with open("./nfc_ant.pretty/%s.kicad_mod" % (modulename), 'w') as f:
        f.write("# ----------------------------------------------------\n")
        f.write("# autogenerated by antGen.py version %s\n" % (SKRIPT_VERSION))
        f.write("# ----------------------------------------------------\n")
        f.write("# used parameters:\n")
        f.write("#   modulename            = %s\n" % (modulename           )) 
        f.write("#   turns                 = %d\n" % (turns                ))
        f.write("#   antennaLength         = %f\n" % (antennaLength        ))
        f.write("#   antennaWidth          = %f\n" % (antennaWidth         ))
        f.write("#   conductorWidth        = %f\n" % (conductorWidth       ))
        f.write("#   conductorSpace        = %f\n" % (conductorSpace       ))
        f.write("#   drillSize             = %f\n" % (drillSize            ))
        f.write("#   minimalConductorSpace = %f\n" % (minimalConductorSpace))
        f.write("#   silkMargin            = %f\n" % (silkMargin           ))
        f.write("#   style                 = %d\n" % (style                ))
        f.write("# ----------------------------------------------------\n")
        f.write(ant)







if __name__ == "__main__":
    main(sys.argv[1:])



