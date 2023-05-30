"""Backup Plus.

Usage:
  app.py backup
  app.py restore
  app.py (-h | --help)
  app.py --version

Options:
  -h --help     View the help document.
  --version     Show version.
"""

from docopt import docopt
from src.backup import start_backup


if __name__ == "__main__":
    arguments = docopt(__doc__, version="v0.0.1")
    # print(arguments)
    if arguments["backup"]:
        start_backup()
    # elif arguments['restore'] :
    #     Install.start_restore()
    else:
        # Show options to user for either backup or restore
        print(
            f"""Press below keys for the Action
        1.  Backup
        2.  Restore
        """
        )
        # Read the argument
        user_input = input("Enter the Option number : ")

        # Check the input
        if user_input.isnumeric:
            if user_input == "1":
                start_backup()
            # elif (input == "2"):
            # Restore.start_restore()
        else:
            print(f"{user_input} : Invlaid input passed, should be a numeric value.")
