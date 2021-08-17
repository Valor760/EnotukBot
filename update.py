import subprocess

def y_n(q):
    while True:
        ri = input(f'{q} (y/n): ')
        if ri.lower() == 'y': return True
        elif ri.lower() == 'n': return False

def main():
    update = y_n("Update the bot?")
    if update:
        try:
            subprocess.check_call('git --version', shell=True, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            raise EnvironmentError("No Git installed!")

        print('Passed Git check.....')

        sp = subprocess.check_output('git status --porcelain', shell=True, universal_newlines=True)
        if sp:
            # oshit = y_n('You have modified files that are tracked by Git (e.g the bot\'s source files).\n'
            #             'Should we try resetting the repo? You will lose local modifications.')
            if False:
                try:
                    subprocess.check_call('git reset --hard', shell=True)
                except subprocess.CalledProcessError:
                    raise OSError("Could not reset the directory to a clean state.")

            try:
                subprocess.check_call('git pull', shell=True)
            except subprocess.CalledProcessError:
                raise OSError("Could not update the bot!")
        else:
            print("No bot updates found!!")


if __name__ == '__main__':
    main()