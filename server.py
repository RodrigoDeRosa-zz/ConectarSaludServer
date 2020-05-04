from tornado.ioloop import IOLoop

from src.database.mongo import Mongo
from src.utils.logging.logger import Logger
from src.utils.argument_parsing.argument_parsing_utils import ArgumentParsingUtils
from src.utils.resource_loading.resource_loader import ResourceLoader
from src.utils.setup.app_creator import AppCreator
from src.utils.setup.server_creator import ServerCreator


def start():
    # Parse command line argument_parsing
    port, processes, db_data = ArgumentParsingUtils.parse_arguments()
    # Set up logger
    Logger.set_up()
    # Create Tornado application
    Logger(__name__).info('Setting up application...')
    app = AppCreator.create_app()
    # Start server on given port and with given processes
    ServerCreator.create(app, port).start(processes)
    # Establish database connection for each process
    Mongo.init(**db_data)
    Mongo.create_indexes()
    app.settings['db'] = Mongo.get()
    # Create basic database entries
    #ResourceLoader.load_resources()
    # Start event loop
    Logger(__name__).info(f'Listening on http://localhost:{port}.')
    IOLoop.current().start()


if __name__ == '__main__':
    start()
