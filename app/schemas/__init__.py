from .accounts \
    import User as UserSchema, \
        UserLoginRequest, \
        UserLoginResponse, \
        UserRegisterRequest, \
        UserRegisterResponse, \
        RoleEnum, \
        UserRegisterWithRole

from .departements \
    import Departement as DepartementSchema, \
        CreateDepartementRequest

from .faculties \
    import Faculty as FacultySchema, \
        CreateFacultyRequest