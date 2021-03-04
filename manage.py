import os
import uvicorn
import argparse

from app import main as application

from app.admin import create_admin
from app.schemas import UserRegisterRequest

# Command line argument definitions
parser = argparse.ArgumentParser(description='Command line interface to interact with the application')
parser.add_argument('main_command', help='Main command, list: run, create-admin, create-migrations, or migrate')
parser.add_argument('-m', '--comment', help='Migrations script command')
parser.add_argument('-e', '--email', help='User email when create admin')
parser.add_argument('-p', '--password', help='User password when create admin')

args = parser.parse_args()

if __name__ == '__main__':
    try:
        if args.main_command == 'run':
            application.run()
        elif args.main_command == 'create-admin':
            user_admin = UserRegisterRequest(
                email=args.email,
                password=args.password
            )
            create_admin(user_admin)
        elif args.main_command == 'create-migrations':
            os.system(f'alembic revision --autogenerate -m "{args.comment}"')
        elif args.main_command == 'migrate':
            os.system('alembic upgrade head')
        elif args.main_command == 'rollback':
            os.system('alembic downgrade head')
        else:
            raise ValueError('The command must be either run or admin')
    except:
        raise Exception('Cannot run input command')