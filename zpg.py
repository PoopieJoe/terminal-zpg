import src.core as core

DEBUGMODE = False

def main():
    game = core.Core()
    game.launch()
    exit()


if __name__ == "__main__":
    if DEBUGMODE:
        import cProfile
        cProfile.run('main()','zpg.prof')
    else:
        main()