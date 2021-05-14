from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Response

from ..config import Envs
from ..dependencies import get_user
from ..models import UserModel, RoleModel
from ..schemas import \
    RoleEnum, \
    UserSchema, \
    UserVerification, \
    UserLoginRequest, \
    UserLoginResponse, \
    ResendEmailRequest, \
    ResendEmailResponse, \
    UserRegisterRequest, \
    UserRegisterResponse, \
    UserRegisterWithRole, \
    ForgotPasswordRequest, \
    ForgotPasswordResponse, \
    ChangePasswordRequest, \
    ChangePasswordResponse


account_router = APIRouter(prefix='/accounts', tags=['accounts'])


@account_router.get('/')
async def index(user: UserSchema = Depends(get_user)):
    return 'This is accounts route index'


@account_router.post('/register/student', response_model=UserRegisterResponse)
async def register_for_student(request: UserRegisterRequest, background_tasks: BackgroundTasks):
    """
    Register a user with all the information:

    - **email**: user email, must be unique
    - **password**: user password
    - **username**: optional
    - **fullname**: optional
    """
    response = await UserModel.register(request, [RoleEnum.STUDENT], background_tasks)
    return response


@account_router.post('/register', response_model=UserRegisterResponse)
async def register_with_role(request: UserRegisterWithRole, user: UserSchema = Depends(get_user)):
    """
    Register a user with all the information:

    - **email**: user email, must be unique
    - **password**: user password
    - **username**: optional
    - **fullname**: optional
    - **role_id**: user's role
    """
    privilage_exception = HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='You are not allowed to create that user')

    if user.role_id == RoleEnum.ADMIN:
        pass
    elif user.role_id == RoleEnum.FACULTY_DEAN and set(request.role_mappings).issubset(RoleModel.roles_list[1:]):
        raise privilage_exception
    elif user.role_id == RoleEnum.HEAD_DEPARTEMENT and set(request.role_mappings).issubset(RoleModel.roles_list[2:]):
        raise privilage_exception
    elif user.role_id == RoleEnum.TEACHER and set(request.role_mappings).issubset(RoleModel.roles_list[3:]):
        raise privilage_exception

    response = await UserModel.register(request)
    return response


@account_router.post('/login', response_model=UserLoginResponse)
async def login(user: UserLoginRequest):
    """
    Login user to get token with these required informations:

    - **email**: user email, must be unique
    - **password**: user password
    """
    response = await UserModel.login(user)
    return response.dict()


@account_router.get('/profile')
async def get_profile(user: UserSchema = Depends(get_user)):
    """
    Get logged in user's data
    """
    return user


@account_router.get('/verify-account')
async def verify_account(email: str, verification_code: str):
    user_verification_data = UserVerification(
        email=email, verification_code=verification_code)
    await UserModel.verify_account(user_verification_data)
    return RedirectResponse(f'{Envs.FRONTEND_URL}/auth/login')


@account_router.post('/resend-email')
async def resend_email(request: ResendEmailRequest, background_tasks: BackgroundTasks):
    await UserModel.resend_email(request.email, background_tasks)
    return ResendEmailResponse(success=True, data={})


@account_router.post('/forgot-password')
async def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks):
    await UserModel.ask_change_password(request.email, background_tasks)
    return ForgotPasswordResponse(success=True, data={})


@account_router.post('/change-password')
async def change_password(request: ChangePasswordRequest, email: str, verification_code: str):
    await UserModel.change_password(request, email, verification_code)
    return ChangePasswordResponse(success=True, data={})
