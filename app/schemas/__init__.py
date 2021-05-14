from typing import Union
from pydantic import BaseModel

from .accounts \
    import User as UserSchema, \
    RoleEnum, \
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

from .departements \
    import Departement as DepartementSchema, \
    CreateDepartementRequest

from .faculties \
    import Faculty as FacultySchema, \
    CreateFacultyRequest

from .classrooms \
    import Classroom as ClassroomSchema, \
    CreateClassroomRequest


class Response(BaseModel):
    success: bool
    message: str
    data: Union[dict, list]
