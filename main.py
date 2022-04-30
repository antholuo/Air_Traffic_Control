########################################
# main.py
#########
# ATC Challenge
# Anthony Luo, January 2022
#########
# Runs everything in different threads
########################################

import threading

from Visualization import visualizer_main

def start_atc():
    # visualization = threading.Thread(target=visualizer_main.run_visualization, args=())

    # visualization.start();

    # visualization.join(); # I don't think that we need to join them..
    return

if __name__ == "__main__":
    start_atc();