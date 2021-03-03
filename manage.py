import sys
import uvicorn

from app import main as application


if __name__ == '__main__':
    main_command = sys.argv[1]  # Must be either run or admin otherwise raise error
    if main_command == 'run':
        application.run()
    elif main_command == 'admin':
        print('This is an admin command')
    else:
        raise ValueError('The command must be either run or admin')