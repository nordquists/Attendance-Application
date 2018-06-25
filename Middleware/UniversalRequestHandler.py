"""
Used to handle server side login operations.

    login:
        Called with a connection to bottleserver/login
        Used to determine if a login is valid
    check_login:
        Called to test a login using a username and a hashed
        password
    create_account:
        Called when a new user would like to claim a username
"""

import security.password as phandler


class UniversalRequestHandler:
    def __init__(self, postgres_handler):
        self.postgres_handler = postgres_handler

    def login(self, username, password):
        """
        Called when a user goes to the /login directory of the bottle server.
        Accepts a JSON formatted request file in the form of:

            type: String ('LOGIN')
            email: String
            password: String

        """
        # Hash the password
        hashed_password = phandler.hash_password(password)
        return self.check_login(username, hashed_password)

    def check_login(self, username, hashed_password):
        """
        Selects correct password hash from sql database and compares them using a
        password_handler.py function.

            username: String
            hashed_password: String

        :returns JSON with format

            successful: boolean
            reason: String
        """

        return_request = {
            'successful': False,
            'classification': 'unknown',
            'reason': 'Unknown'
        }

        try:
            # Select correct password from database based on username
            # Create SQL Queries
            sql_student = "SELECT password FROM student WHERE LOWER(email) = LOWER('%s');" % username
            sql_admin = "SELECT password FROM admin WHERE LOWER(email) = LOWER('%s');" % username

            # Get the correct passwords for students and administrators
            correct_password_student = self.postgres_handler.select(sql_student)
            correct_password_admin = self.postgres_handler.select(sql_admin)

            # If this is an admin (if it exists in the admin table)
            if correct_password_admin:
                # If the account is from an admin set the correct_password to admin's password
                correct_password = correct_password_admin
                return_request['classification'] = 'admin'
            # Otherwise, it is a student (it is in the student table)
            else:
                # If the account is from an student set the correct_password to students's password
                correct_password = correct_password_student
                return_request['classification'] = 'student'

            # If the username exists (if the list is not empty)
            if not len(correct_password) == 0:
                # Are the passwords the same? If they are, return that it was successful
                return_request['successful'] = phandler.compare_passwords(correct_password[0][0], hashed_password)

                # Reason to be printed to user in case of failed login.
                if return_request['successful']:
                    return_request['reason'] = 'Correct login.'
                else:
                    return_request['reason'] = 'inc_login'
            # Otherwise, the username does not exist
            else:
                return_request['reason'] = 'inc_login'

            return return_request
        except:
            # Fail condition: Broad fail condition for failure to connect to database
            return_request['reason'] = 'con_error'
            return return_request

    def create_account(self, name, username, password, conf_password):
        """
        Allows users to claim a username that is not in use. The JSON request
        accepted is in the format:

            name: String
            email: String
            password: String
            conf_password: String

        :returns JSON with format

            successful: boolean
            reason: String

        ** Makes users login again after claiming account. This is because this
        function only adds to the database, it does not perform the login function
        """

        # Instantiating return_request to be sent to client of server
        return_request = {
            'successful': False,
            'reason': 'Unknown'
        }
        # If passwords match
        if password == conf_password:
            sql = "SELECT * FROM student WHERE LOWER(email) = LOWER(%s);"
            _username = (username, )
            # If the email is not in use (not in the database)
            if not self.postgres_handler.query(sql, _username):
                try:
                    # Hashing password using hashlib
                    pw_hash = phandler.hash_password(password)
                    # Adding new user to database: name, username, hashed password
                    sql = "INSERT INTO student (student_id, name, password, email) VALUES (DEFAULT , %s, %s, %s)"
                    args = (name, pw_hash, username)
                    self.postgres_handler.insert(sql, args)

                    return_request['successful'] = True
                    return_request['reason'] = 'Please login again using your credentials.'
                    return return_request
                except:
                    # Fail condition: Broad fail condition for failure to connect to database
                    return_request['reason'] = 'con_error'
                    return return_request
            else:
                # Fail condition: Email (username) in use
                return_request['reason'] = 'email_use'
                return return_request
        else:
            # Fail condition: Passwords do not match
            return_request['reason'] = 'pass_match'
            return return_request
