
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import ChordyApplicationError
from .controllers.base import Base

# configuration defaults
CONFIG = init_defaults('chordy', 'log.logging')
CONFIG['chordy']['foo'] = 'barh'
CONFIG['log.logging']['level'] = 'ERROR'

class ChordyApplication(App):
    """Chordy Application primary application."""

    class Meta:
        label = 'chordy'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
            'tabulate'
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'tabulate'

        # register handlers
        handlers = [
            Base
        ]


class ChordyApplicationTest(TestApp,ChordyApplication):
    """A sub-class of ChordyApplication that is better suited for testing."""

    class Meta:
        label = 'chordy'


def main():
    with ChordyApplication() as app:
        try:
            app.args.add_argument('--ip', required=True, action='store', dest='ip', help='Server IP address')  
            app.args.add_argument('-p', '--port', required=True, action='store', type=int, dest='port', help='Server port number')  
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except ChordyApplicationError as e:
            print('ChordyApplicationError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
