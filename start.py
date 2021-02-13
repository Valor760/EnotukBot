import subprocess
import sys
import platform

def update_library():
    print('Updating libraries....')

    try:
        subprocess.check_call('pip3 install -r requirements.txt', shell=True)
    except subprocess.CalledProcessError:
        raise OSError("Could not update libraries.".format(sys.executable))


def y_n(q):
    while True:
        ri = input(f'{q} (y/n): ')
        if ri.lower() == 'y': return True
        elif ri.lower() == 'n': return False


def main():
    update_library()
    if platform.system() == 'Linux':
        update = y_n("Update the bot?")
        if update:
            try:
                subprocess.check_call('git --version', shell=True, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                raise EnvironmentError("No Git installed!")

            print('Passed Git check.....')

            try:
                subprocess.check_call('git reset --hard', shell=True)
            except subprocess.CalledProcessError:
                raise OSError("Could not reset the directory!")

            try:
                subprocess.check_call('git pull', shell=True)
            except subprocess.CalledProcessError:
                raise OSError("Could not update the bot!")

    from lib.bot import bot
    bot.run()
    #I WAS HERE

if __name__ == '__main__':
    main()