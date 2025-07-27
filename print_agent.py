def opening():
    print('')
    print('Welcome to:')
    print('    __          ________   ')
    print('   / /   ____  / ____/ /_  __')
    print('  / /   / __ \/ /_  / / / / /')
    print(' / /___/ /_/ / __/ / / /_/ / ')
    print('/_____/\____/_/   /_/\__, /  ')
    print('                    /____/  ')
    print('')
    print('Fully automated, configurable random LoFi music generator')
    print('')
    print('')
    print('- Starting Generation       -')
    print('- Using cfg.py              -')


def loaded_presets(p1,p2,p3,p4):
    print('- selecting random presets: -')
    print("")
    print('Keys: ' + p1)
    print('Lead: ' + p2)
    print('Bass: ' + p3)
    print('Pad: ' + p4)
    print("")
    print('- Loaded Presets            -')
    

def scale(s):
    if s == 0:
        print('- Selected Scale: Major     -')
    else:
        print('- Selected Scale: Minor     -')\
    
def exit():
    print('')
    print('Finished generation, thanks for using LoFly')
    print('')
    print('- Username 4D')