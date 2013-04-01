#!/bin/bash
# Dependencies: xsetroot, feh, rox (pinboard), bash, yad, grep, cat, sed
# File Name: login_background.sh
# Version: 2.0
# Purpose:  controls the setting of backgrounds for default antiX window managers through feh / rox / xsetroot
# Authors: John, Dave

# Copyright (C) antiXCommunity http://antix.freeforums.org
# License: gplv2
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
################################################################################
#################################################################

type="$(cat $HOME/.antix-session/wallpaper.conf | grep '^TYPE' |cut -d '=' -f2 |cut -d " " -f2)"
style="$(cat $HOME/.antix-session/wallpaper.conf | grep '^STYLE' |cut -d '=' -f2 |cut -d " " -f2)"
session=$DESKTOP_CODE;

random_select() {
	WALLPAPERS="$(cat $HOME/.antix-session/wallpaper.conf | grep '^FOLDER' |cut -d '=' -f2 |cut -d " " -f2)"
    ALIST=( `ls -w1 $WALLPAPERS` )
    RANGE=${#ALIST[*]}
    SHOW=$(( $RANDOM % $RANGE ))
    FILE="$WALLPAPERS/${ALIST[$SHOW]}"
    SEDFILE=${FILE//\//\\\/}
    sed -i "s/^$session=.*/$session=$SEDFILE/" $HOME/.antix-session/wallpaper-list.conf 
}
wallpaper_set() {
	
    local style=$1
    local pboard=$2
    
    wallpaper=$(cat $HOME/.antix-session/wallpaper-list.conf | grep "^$session" |cut -d '=' -f2 |sed "s/\ /\\ /ig")
    
    if expr match "$session" "^rox-" &>/dev/null; then
    Rox-Wallpaper "$wallpaper" &
    feh  --bg-scale "$wallpaper" &
    elif expr match "$session" "^space-" &>/dev/null; then
    spacefm --set-wallpaper "$wallpaper" &
    else
    feh  --bg-$style "$wallpaper" &
    fi
    
    #sleep 2 && ~/.antix-session/wallpaper/refresh-list &

}
set_type() {

    local type=$1

    case "$type" in
        random)
			random_select
			wallpaper_set "$style"
            ;;

        random-time)
            yad --notification --command="killall 'login_background.sh' 'yad'" --text="click this icon to kill random wallpaper timed" --image="wallpaper" & pid1="$!"
			while true; do
			    random_select
			    wallpaper_set "$style"
			    sleep 300
			done
            ;;

        static)
            wallpaper_set "$style"
            ;;

        color)
            imported_color=$(cat $HOME/.antix-session/wallpaper.conf | grep '^COLOR' |cut -d '=' -f2 |cut -d " " -f2)
            xsetroot -solid "#$imported_color" &
            ;;

        *)
			echo "Color black has been set as default choice, $type not an option";
			xsetroot -solid "#8a8a8a";
			rox --pinboard="default"
            ;;
    esac
}

set_type "$type"

exit
