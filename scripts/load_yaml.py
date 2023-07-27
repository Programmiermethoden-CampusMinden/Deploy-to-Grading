# Loads configuration data from a yaml file. It is used to load both the
# assignment configuration and the task configurations. This script can be
# imported by anther python script. For detailed information, see the usage
# example or the documentation of the `load_yaml` function:
#
# usage:
# ```python
# from .load_yaml import load_yaml
# from yaml import YAMLError
#
# try:
#     env_vars = load_yaml(path, prefix)
# except (FileNotFoundError, YAMLError) as err:
#     pass # Handle exceptions here
# ```
#
# This script is step 1 and step 3 in the Deploy-to-Grading pipeline.
#

import sys
import yaml

def _read_yaml(filename):
    # Reads yaml data from given filename. Returns yaml data object.
    # Throws FileNotFoundError or yaml.YAMLError on error.
    with open(filename, "r") as file:
        return yaml.safe_load(file)

def _get_env_prefix(filename, custom_prefix):
    # Returns either the argument specified or converts the filename
    # with path and file extension to the prefix.
    # In both cases, the prefix is converted to uppercase.
    if custom_prefix is not None:
        return custom_prefix.upper()

    size = len(filename)
    start = 0
    if '/' in filename:
        start = size - filename[size:0:-1].index('/', 0, size)
    end = size - filename[size:0:-1].index('.', 0, size) - 1
    return filename[start:end].upper()

def _get_env_variables(yaml_data, prefix):
    # Create environment variable dictionary from yaml data
    env_vars = {}
    for key in yaml_data:
        value = yaml_data[key]
        if isinstance(value, str) or isinstance(value, int) or \
                isinstance(value, float):
            env_vars["%s_%s" % (prefix, key.upper())] = str(value)
        elif isinstance(value, list):
            if isinstance(value[0], str) or isinstance(value, int) \
                    or isinstance(value, float):
                # Export list of values as a string with values seperated by a space
                env_vars["%s_%s" % (prefix, key.upper())] = " ".join(value)
            elif isinstance(value[0], dict):
                keys = []
                for v in value:
                    keys.extend(v.keys())
                    env_vars.update(_get_env_variables(v, "%s_%s" % (prefix, key.upper())))
                env_vars["%s_%s" % (prefix, key.upper())] = " ".join(keys)
            else:
                print("echo \"Unknown type (%s)\"" % type(value), file=sys.stderr)
        elif isinstance(value, dict):
            env_vars.update(_get_env_variables(value, "%s_%s" % (prefix, key.upper())))
        else:
            # Printing this with echo so that it does not break the other
            # exports.
            print("echo \"Unknown type (%s)\"" % type(value), file=sys.stderr)
    return env_vars


def load_yaml(yaml_path, prefix=None):
    """
    Loads configuration as environment variable array from the given yaml file.

    Parameters:
    yaml_path (string): Path to the yaml file to load
    prefix (string): Prefix to use for the environment variables (Default: filename)

    Returns:
    dict: Environment variables and their values
    """
    yaml_data = _read_yaml(yaml_path)
    env_prefix = _get_env_prefix(yaml_path, prefix)
    return _get_env_variables(yaml_data, env_prefix)

