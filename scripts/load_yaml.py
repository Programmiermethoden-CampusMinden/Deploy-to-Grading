#!/bin/python3

import sys
import yaml

def print_usage():
    print("usage: load_yaml.py [filename] [prefix(optional)]")
    print("       After execution, source the output to add the variables")
    print("       to the environment.")
    exit(-1)

def get_filename():
    # Get filename from argv. Appends file extension if necessary.
    # Returns filename. Does not return on error.
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        filename = sys.argv[1]

        if not filename.endswith(".yml"):
            filename += ".yml"
        return filename
    print_usage()

def read_yaml(filename):
    # Reads yaml data from given filename.
    # Returns yaml data object. Does not return on error.
    try:
        with open(filename, "r") as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as err:
                print("Invalid yaml file")
                print_usage()
    except FileNotFoundError as err:
        print("File %s not found" % filename)
        print_usage()

def get_env_prefix(filename):
    # Returns either the argument specified or converts the filename
    # with path and file extension to the prefix.
    # In both cases, the prefix is converted to uppercase.
    if len(sys.argv) == 3:
        return sys.argv[2].upper()

    size = len(filename)
    start = size - filename[size:0:-1].index('/', 0, size)
    end = size - filename[size:0:-1].index('.', 0, size) - 1
    return filename[start:end].upper()

def print_env_variables(yaml_data, prefix):
    # Print environment variables to shell so they can be
    # loaded by a shell script to the parent shell environment.
    for key in yaml_data:
        value = yaml_data[key]
        if isinstance(value, str):
            print("export %s_%s=%s" % (prefix, key.upper(),
                    value.replace(" ", "\ ")))
        elif isinstance(value, int) or isinstance(value, float):
            print("export %s_%s=%s" % (prefix, key.upper(), value))
        elif isinstance(value, list):
            if isinstance(value[0], str) or isinstance(value, int) \
                    or isinstance(value, float):
                # TODO: This is currently just a workaround that might
                # not work.
                print("export %s_%s=%s" % (prefix, key.upper(),
                        "\ ".join(value)))
            elif isinstance(value[0], dict):
                keys = []
                for v in value:
                    keys.extend(v.keys())
                    print_env_variables(v, "%s_%s" % (prefix, key.upper()))
                print("export %s_%s=%s" % (prefix, key.upper(),
                        "\ ".join(keys)))
            else:
                print("echo \"Unknown type type(%s)\"" % type(value))
        elif isinstance(value, dict):
            #print("export %s_%s=%s" % (prefix, key.upper(),
            #        "\ ".join(value.keys())))
            print_env_variables(value, "%s_%s" % (prefix, key.upper()))
        else:
            # Printing this with echo so that it does not break the other
            # exports.
            print("echo \"Unknown type type(%s)\"" % type(value))

def main():
    filename = get_filename()
    yaml_data = read_yaml(filename)
    print_env_variables(yaml_data, get_env_prefix(filename))

if __name__ == "__main__":
    main()
