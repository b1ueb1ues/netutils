#!/bin/bash

create_ap --stop `create_ap --list-running |grep "[0-9]"|awk '{print $1}'`

