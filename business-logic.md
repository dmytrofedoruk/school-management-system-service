Let's say you are a student, so your role for this application is as student:
1. Create an account, by registering. On register page, user has to fill their username, email, password, faculty, and departement.
2. An email will be sent to your email address
3. Validate your account by clicking the button on validation email we sent
4. After you validate your, actually you are not yet a valid student. 
5. You need approvals from faculty staff and departement staff.
6. After faculty staff dan departement staff approved your application. Then you are approved.
7. Now, you account is validated and you can login
8. After you login, you have to fill two fields about which faculty you want to be enrolled in and which departement
9. At this point, you are not capable to access several pages on the application. Since you are not yet an eligible student. But you can still see the home page, the list faculties, the list of departements, News(?).
10. List of pages:
    - Register
    - Login
    - Send email
    - Forgot Password
    - Change password

New Tasks:
- New field on user's table called 'approved'
- Create a table of faculties_students contains faculty_id, student_id, approved
- Create a table of departements_students contains departement_id, student_id, approved
- Create table roles
- Create table authorizations
- New field on departement's table called 'faculty_id'
- New field on class' table called 'departement_id'
- Create table to connect teacher and faculty
- Create table to connect teacher and departement