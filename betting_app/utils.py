def read_config(config_file='config.ini'):
    import os
    import configparser

    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory
    parent_dir = os.path.dirname(current_dir)

    # Construct the path to the config.ini file
    config_path = os.path.join(parent_dir, config_file)

    config = configparser.ConfigParser()
    config.read(config_path)

    return config