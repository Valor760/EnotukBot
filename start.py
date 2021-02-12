from lib.bot import bot
import subprocess
import sys


try:
    subprocess.check_call('"{}" -m pip install --no-warn-script-location --user -U -r requirements.txt'.format(sys.executable), shell=True)

except subprocess.CalledProcessError:
    raise OSError("Could not update dependencies.".format(sys.executable))

bot.run()