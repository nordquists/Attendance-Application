"""
config/connector.py is the file that provides reading and writing writes to
the database configuration file.
"""
import json

CONFIG_FILE = 'db.config'


def write_data(item, value):
    """
    Writes data to item of CONFIG_FILE with the parameter value.

    :returns success/error information in JSON object
    """
    try:
        if CONFIG_FILE is not None:
            config = json.load(open(CONFIG_FILE))
            config[item] = value
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, ensure_ascii=False)
        return {
            'successful': True,
            'reason': 'Successfully written {' + str(item) + ': ' + str(value) + '} to config.'
        }
    except IOError:
        return {
            'successful': False,
            'reason': 'File \'' + CONFIG_FILE + '\' not found. Unable to write {' + str(item) + ': ' + str(
                value) + '} to config. '
        }
    except:
        return {
            'successful': False,
            'reason': 'Unknown Error. Unable to write {' + str(item) + ': ' + str(value) + '} to config.'
        }


def read_data(item):
    """
    Reads data (item) from CONFIG_FILE.

    :returns item data and success/error information in JSON object
    """
    try:
        if CONFIG_FILE is not None:
            config = json.load(open(CONFIG_FILE))
            return {
                item: config[item],
                'successful': True,
                'reason': 'Successfully read {' + str(config[item]) + '} from config.'
            }
    except IOError:
        return {
            'successful': False,
            'reason': 'File \'' + CONFIG_FILE + '\' not found. Unable to read {' + str(item) + '} from config. '
        }
    except:
        return {
            'successful': False,
            'reason': 'Unknown Error. Unable to read {' + str(item) + '} from config.'
        }
