#!/bin/python3

import sys
import yaml

def _print_usage():
    if __name__ == "__main__":
        print("usage: load_yaml.py [filename] [prefix(optional)]")
        print("       After execution, source the output to add the variables")
        print("       to the environment.")
        print("")
        print("       Params:")
        print("       filename    Path to the yaml file")
        print("       prefix      Optional prefix of the env variables (default: name of the file)")
        exit(-1)
    else:
        raise RuntimeError("Failed to load yaml file.")

def _get_filename(argv):
    # Get filename from argv. Appends file extension if necessary.
    # Returns filename. Does not return on error.
    if len(argv) == 2 or len(argv) == 3:
        filename = argv[1]

        if not filename.endswith(".yml"):
            filename += ".yml"
        return filename
    _print_usage()

def _read_yaml(filename):
    # Reads yaml data from given filename.
    # Returns yaml data object. Does not return on error.
    try:
        with open(filename, "r") as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as err:
                print("Invalid yaml file")
                _print_usage()
    except FileNotFoundError as err:
        print("File %s not found" % filename)
        _print_usage()

def _get_env_prefix(filename, argv):
    # Returns either the argument specified or converts the filename
    # with path and file extension to the prefix.
    # In both cases, the prefix is converted to uppercase.
    if len(argv) == 3 and argv[2] is not None:
        return argv[2].upper()

    size = len(filename)
    start = 0
    if '/' in filename:
        start = size - filename[size:0:-1].index('/', 0, size)
    end = size - filename[size:0:-1].index('.', 0, size) - 1
    return filename[start:end].upper()

def _print_env_variables(env_variables):
    # Print environment variables to shell so they can be
    # loaded by a shell script to the parent shell environment.
    for key in env_variables:
        print("export %s=%s" % (key, env_variables[key]))

def _get_env_variables(yaml_data, prefix):
    # Create environment variable dictionary from yaml data
    env_vars = {}
    for key in yaml_data:
        value = yaml_data[key]
        if isinstance(value, str):
            env_vars["%s_%s" % (prefix, key.upper())] = value.replace(" ", "\ ")
        elif isinstance(value, int) or isinstance(value, float):
            env_vars["%s_%s" % (prefix, key.upper())] = value
        elif isinstance(value, list):
            if isinstance(value[0], str) or isinstance(value, int) \
                    or isinstance(value, float):
                # Export list of values as a string with values seperated by a space
                env_vars["%s_%s" % (prefix, key.upper())] = "\ ".join(value)
            elif isinstance(value[0], dict):
                keys = []
                for v in value:
                    keys.extend(v.keys())
                    env_vars.update(_get_env_variables(v, "%s_%s" % (prefix, key.upper())))
                env_vars["%s_%s" % (prefix, key.upper())] = "\ ".join(keys)
            else:
                print("echo \"Unknown type (%s)\"" % type(value))
        elif isinstance(value, dict):
            env_vars.update(_get_env_variables(value, "%s_%s" % (prefix, key.upper())))
        else:
            # Printing this with echo so that it does not break the other
            # exports.
            print("echo \"Unknown type (%s)\"" % type(value))
    return env_vars


def parse_env_variables(path, prefix=None):
    # Parse environment variables from the given path
    # Set the prefix for a different value than the filename
    argv = ["load_yaml", path, prefix]
    filename = _get_filename(argv)
    yaml_data = _read_yaml(filename)
    env_prefix = _get_env_prefix(filename, argv)
    env_vars = _get_env_variables(yaml_data, env_prefix)
    _print_env_variables(env_vars)

def _main():
    filename = _get_filename(sys.argv)
    yaml_data = _read_yaml(filename)
    env_prefix = _get_env_prefix(filename, sys.argv)
    env_vars = _get_env_variables(yaml_data, env_prefix)
    _print_env_variables(env_vars)

if __name__ == "__main__":
    _main()
