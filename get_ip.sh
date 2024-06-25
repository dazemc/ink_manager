#!bin/bash
hostname -I | awk '{print $1}'
exit