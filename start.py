import subprocess
import sys
import platform

def update_library():
    print('Updating libraries....')

    if platform.system() == 'Linux':
        try:
            subprocess.check_call('pip3 install -r requirements.txt', shell=True)
        except subprocess.CalledProcessError:
            raise OSError("Could not update libraries.".format(sys.executable))

    elif platform.system() == 'Windows':
        try:
            subprocess.check_call('"{}" -m pip install --no-warn-script-location --user -U -r requirements.txt'.format(sys.executable), shell=True)
        except subprocess.CalledProcessError:
            raise OSError("Could not update libraries.".format(sys.executable))


def main():
    update_library()
    from lib.bot import bot
    bot.run()

if __name__ == '__main__':
    main()