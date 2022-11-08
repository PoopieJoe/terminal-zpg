import sys
import src.core as core
import tkinter as tk
DEBUGMODE = False

def main():
    game = core.Core()
    game.launch()

if __name__ == "__main__":
    if DEBUGMODE:
        import cProfile
        cProfile.run('main()','zpg.prof')
    else:
        main()
    sys.exit()