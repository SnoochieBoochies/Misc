#!/bin/bash

scrot /tmp/tempshot.png
convert /tmp/tempshot.png -blur 0x5 /tmp/screenshot.png
i3lock -i /tmp/screenshot.png
