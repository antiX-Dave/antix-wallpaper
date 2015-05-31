#!/bin/bash
# Filename:      pinboardtoggle.sh
# Purpose:       toggle Rox pinboard on/off from menu
# Authors:       Kerry and anticapitalista for antiX
# Modified:      Dave (david@daveserver.info) 
# Latest change: Tuesday April 9, 2013.
################################################################################

APP_DIR=`dirname "$0"` export APP_DIR
PASSED="$1";
DESKTOP_CODE=$(cat ~/.antiX-session/desktop-code$DISPLAY);
DESKTOP=$(echo $DESKTOP_CODE |sed "s/^.*-//ig");

if expr match "$DESKTOP_CODE" "^rox-" &>/dev/null; then
    DESKTOP_CODE="$DESKTOP";
    echo "$DESKTOP_CODE" > ~/.antiX-session/desktop-code$DISPLAY
    exec rox -p= ;
elif expr match "$DESKTOP_CODE" "^space-" &>/dev/null; then
    DESKTOP_CODE="$DESKTOP";
    echo "$DESKTOP_CODE" > ~/.antiX-session/desktop-code$DISPLAY
    killall spacefm ;
else
    echo $PASSED
    DESKTOP_CODE="$PASSED-$DESKTOP";
    echo "$DESKTOP_CODE" > ~/.antiX-session/desktop-code$DISPLAY  
    case "$PASSED" in 
        rox)
        exec rox -p=antiX-$DESKTOP;
        ;;
        space)
        killall spacefm;
        exec spacefm --desktop &
        ;;
        *)
        yad --image="error" --text="Error: Toggle script has not recieved a valid icon manager code" --button="gtk-ok:0" &
        ;;
    esac
fi
login_background.sh
