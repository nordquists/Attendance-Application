"""
Request functions available to student users.
"""
import datetime


class StudentRequestHandler:
    def __init__(self, postgres_handler):
        self.postgres_handler = postgres_handler

    def update_location(self, username, major, minor):
        """
        Allows students to update their location based on the major and minor keys of
        the beacon closest to them. The JSON request accepts:

            username: String
            Major: String (int8)
            Minor: String (int8)

        :returns JSON response with format

            successful: Boolean
            reason: String
            closest_beacon: String
            beacon_description: String
        """

        # Surround with try/except in case of connection errors
        try:
            # The major and minor values first have to be matched to a beacon
            # Create SQL Query string
            sql = "SELECT * FROM beacon WHERE major_key = (%s) AND minor_key = (%s);"
            args = (major, minor,)
            # Beacon received
            beacon = self.postgres_handler.query(sql, args)[0]

            # Then, the student_id value must be obtained.
            # Create SQL Query string
            sql = "SELECT * FROM student WHERE email = (%s);"
            # Format item to be searched for
            username = (username,)
            # Student received
            student = self.postgres_handler.query(sql, username)[0]
            # Student_id obtained
            student_id = student[0]

            # Lastly, the location must be added to the database with the student,
            # beacon id, and a server time timestamp.
            # Create time stamp for current time and convert it to a string.
            timestamp = str(datetime.datetime.now())
            # Create SQL Query string
            sql = "INSERT INTO location (location_id , time_stamp, closest_beacon_id, student_student_id) VALUES (DEFAULT, %s, %s, %s)"
            args = (timestamp, beacon[0], student_id)
            self.postgres_handler.insert(sql, args)

            return {
                'successful': True,
                'reason': 'success',
                # Pass the 'closest_beacon' item the beacon room number
                'closest_beacon': beacon[1],
                'beacon_description': beacon[2]
            }
        except:
            print("Failed to update location")


    def get_info(self, username):
        """
        Allows students to get information about themselves to be displayed on
        their screen. The JSON request accepts only one variable:

            username: String

        :returns JSON response with format

            successful: Boolean
            reason: String
            name: String
            email: email
        """

        # We know that the username exists in the database, because it has already been
        # used to login. So, we can simply make a request without worries of errors.

        # We still surround it with a try/except in case of connection errors.
        try:
            # Create SQL Query string
            sql = "SELECT * FROM student WHERE email = (%s);"
            # Format item to be searched for
            username = (username,)
            student = self.postgres_handler.query(sql, username)[0]

            return {
                'successful': True,
                'reason': 'success',
                'name': student[1],
                'email': student[3]
            }
        except:
            # Fail condition: Broad fail condition for a connection to database error.
            return {
                'successful': False,
                'reason': 'Connection Error.',
                'name': 'error',
                'email': 'error',
            }
