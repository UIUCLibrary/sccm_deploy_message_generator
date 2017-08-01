import argparse
import copy

import sys

from .generate import get_message_data, generate_message, get_footer


def get_parser():
    args = argparse.ArgumentParser()
    args.add_argument("settings", type=argparse.FileType(), help="YAML file with deployment information")

    override = args.add_argument_group("override")
    override.add_argument("--deployer", help="name of deployment contact")
    override.add_argument("--pkgname", dest="package_name", help="package file name")
    override.add_argument("--pkgpath", dest="package_path", help="package file path")
    override.add_argument("--maintname", dest="maintainer_name", help="package maintainer's name")
    override.add_argument("--maintemail", dest="maintainer_email", help="package maintainer's contact email")
    args.add_argument("--save", type=argparse.FileType("w"), help="Save message to a file")
    return args


def update_message(message_data, args):
    new_data = copy.copy(message_data)
    if args.deployer:
        new_data.receiver_name = args.deployer

    if args.package_name:
        new_data.package_filename = args.package_name

    if args.package_path:
        new_data.package_path = args.package_path

    if args.maintainer_name:
        new_data.maintainer_name = args.maintainer_name

    if args.maintainer_email:
        new_data.maintainer_email = args.maintainer_email

    return new_data


def main():
    parser = get_parser()
    args = parser.parse_args()
    args.settings.close()  # FileType opens the file but there is need for that. Just need the file name
    original_message_data = get_message_data(args.settings.name)
    updated_message_data = update_message(original_message_data, args)
    try:
        body = generate_message(updated_message_data)
        footer = get_footer()
        message = "{}\n\n\n{}".format(body, footer)
    except TypeError:
        print("Unable to build message because {} contains errors.".format(args.settings.name), file=sys.stderr)
        exit(sys.exit(1))


    if args.save:
        args.save.write(message)
        args.save.write("\n")
    else:
        print(message)


if __name__ == '__main__':
    main()
