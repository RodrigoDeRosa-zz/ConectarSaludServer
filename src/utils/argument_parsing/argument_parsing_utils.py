from argparse import ArgumentParser


class ArgumentParsingUtils:

    @classmethod
    def parse_arguments(cls):
        """ Get environment from program argument_parsing. tornado.options could be used instead of ArgumentParser. """
        parser = ArgumentParser()
        # Set up argument values
        parser.add_argument('--proc', nargs='?', default=1, type=int, help='Number of processes. 0 is one per CPU.')
        parser.add_argument('--port', nargs='?', default=5000, type=int, help='Port where application will listen.')
        parser.add_argument('--db_host', nargs='?', default='localhost', help='MongoDB host.')
        parser.add_argument('--db_port', nargs='?', default=27017, type=int, help='MongoDB port.')
        parser.add_argument('--db_name', nargs='?', default='connecting_health', help='MongoDB database name.')
        parser.add_argument('--db_user', nargs='?', default=None, help='MongoDB authentication user.')
        parser.add_argument('--db_password', nargs='?', default=None, help='MongoDB authentication password.')
        # Get program argument_parsing
        args = parser.parse_args()
        # Create DB data dictionary
        db_data = dict()
        db_data['host'] = args.db_host
        db_data['port'] = args.db_port
        db_data['db_name'] = args.db_name
        db_data['user'] = args.db_user
        db_data['password'] = args.db_password
        return args.port, args.proc, db_data
