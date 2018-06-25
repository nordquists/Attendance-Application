"""
Request functions available to administrator users.
"""
import security.password as phandler


class AdminRequestHandler:
    def __init__(self, postgres_handler):
        self.postgres_handler = postgres_handler

    def get_students(self, query=None):
        """
            Function called to get all students.

            :returns JSON with format

                successful: boolean
                students: [student dictionary object]
        """
        sql = "SELECT * FROM student"
        results = self.postgres_handler.select(sql)
        results_formatted = []
        for student in results:
            results_formatted.append({'name': student[1], 'email': student[3], 'id': str(student[0])})
        print(results_formatted)
        return {
            'students': results_formatted,
            'successful': True
        }

    def get_student_location(self, student_id):
        """
            Function called to get all locations given a student. Accepts JSON with
            format:

                student_id: String

            :returns JSON with format

                successful: boolean
                results: [location dictionary object]
        """
        if student_id:
            # Precondition: Ensure that student_id is not equal to None
            # Create SQL query and prepare it to be concatenated
            sql = "SELECT * FROM location WHERE student_student_id = (%s);"
            student_id = (student_id,)
            locations = self.postgres_handler.query(sql, student_id)
            locations_formatted = []
            if locations:
                for location in locations:
                    sql = "SELECT * FROM beacon WHERE beacon_id = (%s);"
                    beacon_id = (str(location[2]),)
                    beacon = self.postgres_handler.query(sql, beacon_id)[0]

                    sql = "SELECT * FROM zone WHERE zone_id = (%s);"
                    zone_id = (str(beacon[5]),)
                    zone = self.postgres_handler.query(sql, zone_id)[0]

                    locations_formatted.append({'room_number': beacon[1], 'zone_id': str(zone[0]), 'description': str(beacon[2]), 'timestamp': location[1]})
            return {
                'results': locations_formatted,
                'successful': True
            }
        return {
            'successful': False,
            'reason': 'No student_id provided'
        }

    def get_zones(self, query):
        """
            Function called to get all zones.

            :returns JSON with format

                successful: boolean
                zones: [zone dictionary object]
        """
        sql = "SELECT zone_name FROM zone"
        results = self.postgres_handler.select(sql)
        results_formatted = []
        for zone in results:
            results_formatted.append(str(zone[0]))

        print(results_formatted)
        return {
            'zones': results_formatted,
            'successful': True
        }

    def get_beacons(self, query):
        """
            Function called by a IOS admin to get all beacons.

            :returns JSON with format

                successful: boolean
                beacons: [beacon dictionary object]
        """
        sql = "SELECT * FROM beacon"
        beacons = self.postgres_handler.select(sql)
        results_formatted = []
        for beacon in beacons:
            # We need zone names as well, all we have are the zone_ids
            sql = "SELECT zone_name FROM zone WHERE zone_id = %s"
            zone_id = (beacon[5],)
            zone_name = self.postgres_handler.query(sql, zone_id)[0][0]
            results_formatted.append({'room_number': beacon[1], 'description': beacon[2], 'id': str(beacon[0]), 'zone_name': zone_name})
        print(results_formatted)
        return {
            'beacons': results_formatted,
            'successful': True
        }

    def get_beacons_macos(self, query):
        """
            Function called by a MACOS admin to get all beacons.

            :returns JSON with format

                successful: boolean
                beacons: [beacon dictionary object]
        """
        sql = "SELECT * FROM beacon"
        beacons = self.postgres_handler.select(sql)
        results_formatted = []
        for beacon in beacons:
            # We need zone names as well, all we have are the zone_ids
            sql = "SELECT zone_name FROM zone WHERE zone_id = %s"
            zone_id = (beacon[5],)
            zone_name = self.postgres_handler.query(sql, zone_id)[0][0]
            results_formatted.append(
                {'room_number': beacon[1], 'description': beacon[2], 'id': str(beacon[0]), 'zone_name': zone_name, 'major': str(beacon[3]), 'minor': str(beacon[4])})
        print(results_formatted)
        return {
            'beacons': results_formatted,
            'successful': True
        }

    def create_beacon(self, room_number, zone_name, description):
        """
            Function called by admin to create a new beacon. Automatically generates the major and minor values to be
            used as the identifier of the beacon. A JSON request is accepted in the format:

                room_number: String
                description: String
                zone_name: String

            :returns JSON with format

                successful: boolean
                reason: String
        """
        # Must generate a unique set of major and minor values
        major_value = 0
        # minor_value definition automatic.
        # Uses POSTGRESQL's SERIAl property to increment value of minor key, with uniqueness validation.
        # Minor value now unique, major unnecessary to change as per minor's 2^16 size -- impractical to fill all slots.

        # zone_id is what is necessary; so, firstly, get zone_id from zone_name (it is unique)
        sql = "SELECT zone_id FROM zone WHERE zone_name = (%s)"
        zone_name = (zone_name,)
        # Obtained zone_id
        zone_id = self.postgres_handler.query(sql, zone_name)[0][0]

        args = (room_number, description, major_value, zone_id)
        sql = "INSERT INTO beacon (beacon_id, room_number, description, major_key, minor_key, zone_zone_id) VALUES (DEFAULT , %s, %s, %s, DEFAULT, %s)"

        self.postgres_handler.insert(sql, args)

        return {
            'successful': True,
            'reason': 'No query provided'
        }

    def edit_beacon(self, beacon_id, room_number=None, description=None, zone_name=None):
        """
            Allows an admin to edit a beacon from the database. A JSON request
            is accepted in the format:

                beacon_id: String
                room_number: String
                description: String
                zone_name: String

            :returns JSON with format

                successful: boolean
                reason: String
        """
        if beacon_id:
            # Precondition: Ensure that beacon_id is not equal to None
            if room_number:
                sql = "UPDATE beacon SET room_number = '%s' WHERE beacon_id = '%s';" % (room_number, beacon_id)
                self.postgres_handler.update(sql),
            if description:
                sql = "UPDATE beacon SET description = '%s' WHERE beacon_id = '%s';" % (description, beacon_id)
                self.postgres_handler.update(sql),
            if zone_name:
                # zone_id is what is necessary; so, firstly, get zone_id from zone_name (it is unique)
                sql = "SELECT zone_id FROM zone WHERE zone_name = (%s)"
                zone_name = (zone_name,)
                # Obtained zone_id
                zone_id = self.postgres_handler.query(sql, zone_name)[0][0]

                # Use this to update the beacon
                sql = "UPDATE beacon SET zone_zone_id = %s WHERE beacon_id = %s;"
                args = (zone_id, beacon_id)
                self.postgres_handler.insert(sql, args)
            return {
                'successful': True,
                'reason': 'Edit(s) made.'
            }
        return {
            'successful': False,
            'reason': 'No query provided'
        }

    def delete_beacon(self, beacon_id):
        """
            Allows an admin to delete a beacon from the database. A JSON request
            is accepted in the format:

                beacon_id: String

            :returns JSON with format

                successful: boolean
                reason: String
        """
        if beacon_id:
            # Precondition: Ensure that beacon_id is not equal to None
            sql = "DELETE FROM beacon WHERE beacon_id = %s;"
            self.postgres_handler.query(sql, beacon_id)

            return {
                'successful': True,
                'reason': 'Beacon deleted'
            }
        return {
            'successful': False,
            'reason': 'No query provided'
        }

    def add_admin(self, name, username, password, conf_password):
        """
            Allows an admin to add another admin to the database. The JSON request
            accepted is in the format:

                name: String
                email: String
                password: String
                conf_password: String

            :returns JSON with format

                successful: boolean
                reason: String
            """

        # Instantiating return_request to be sent to client of server
        return_request = {
            'successful': False,
            'reason': 'Unknown'
        }
        # If passwords match
        if password == conf_password:
            sql = "SELECT * FROM admin WHERE LOWER(email) = LOWER(%s);"
            _username = (username,)
            # If the email is not in use (not in the database)
            if not self.postgres_handler.query(sql, _username):
                try:
                    # Hashing password using hashlib
                    pw_hash = phandler.hash_password(password)
                    # Adding new user to database: name, username, hashed password
                    sql = "INSERT INTO admin (admin_id, name, password, email) VALUES (DEFAULT , %s, %s, %s)"
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