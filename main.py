def install_requirements(requirements_file):
    """
        Function For Install Requirements
    """
    import subprocess
    with open(requirements_file) as f:
        requirements = f.read().splitlines()
    subprocess.check_call(['pip', 'install', '-r', requirements_file])
    print("All requirements have been installed.")

try:
    import pygame
except:
    install_requirements('req.txt')


from window import WindowVisualizer

def start():
    window = WindowVisualizer(1000, 500)
    print("Please Enter Number Of Bricks ?")
    try:
        number = int(input())
    except:
        print("Wrong format")
        start()
        return
    window.set_bricks_number(number)
    window.start()


start()
