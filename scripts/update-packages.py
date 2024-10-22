#!/usr/bin/python3
# SPDX-FileCopyrightText: 2024 KUNBUS GmbH
# SPDX-License-Identifier: GPL-2.0-or-later
"""Update versions of dependencies in package.json to the most recent ones."""
from argparse import ArgumentParser
from json import dumps, loads
from os.path import dirname, join
from sys import stderr, stdout
from urllib.error import URLError
from urllib.request import urlopen

__version__ = "0.1.0"

PACKAGE_JSON = join(dirname(__file__), "..", "package.json")


def get_npm_package_version(package_name) -> str:
    url = f"https://registry.npmjs.org/{package_name}"

    try:
        with urlopen(url) as response:
            if response.status == 200:
                data = response.read()
                package_info = loads(data)
                return package_info.get("dist-tags", {}).get("latest", "")
    except URLError:
        pass

    return ""


def get_package_json() -> dict:
    with open(PACKAGE_JSON, "r") as file:
        return loads(file.read())


def main(dry_run=False) -> int:
    """
    Compare version of package.json and npm registry.

    Status codes are:
        0 - No new version available
        1 - New version found and updated package.json
        2 - Error fetching version from npm or package.json
    :return: Status code
    """
    dc_package_lock = get_package_json()
    new_version = False

    for dependency in dc_package_lock.get("dependencies", {}).keys():
        package_name = dependency
        package_npm_version = get_npm_package_version(package_name)
        package_json_version = dc_package_lock.get("dependencies", {}).get(package_name)

        if not package_npm_version:
            stderr.write(
                f"Could not fetch version of {package_name} from registry.npmjs.org.\n"
            )
            return 2
        if not package_json_version:
            stderr.write(
                f"Could not fetch version of {package_name} in package.json.\n"
            )
            return 2

        if package_json_version != package_npm_version:
            new_version = True
            dc_package_lock["dependencies"][package_name] = package_npm_version
            stdout.write(
                f"Updating version of {package_name} from {package_json_version} to {package_npm_version}\n"
            )

    if new_version:
        if not dry_run:
            with open(PACKAGE_JSON, "w") as file:
                file.write(dumps(dc_package_lock, indent=2))

            stdout.write(
                "Updated package.json, do not forget to run 'make update-all' command.\n"
            )
        return 1

    return 0


if __name__ == "__main__":
    # Generate command arguments of the program
    parser = ArgumentParser(
        prog="update-packages",
        description="Use this program to update the package.json dependencies to the most recent ones.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Run program without modifying package.json file.",
    )
    parser.add_argument(
        "--success",
        choices=["updates", "current"],
        default="updates",
        help="Return exit code 0 depending of availability of updates. This could help in CI pipelines.",
    )
    args = parser.parse_args()

    status_code = main(args.dry_run)

    # Modify exit code of application depending on set arguments
    if args.success == "current" and status_code == 0:
        exit(0)
    elif args.success == "updates" and status_code == 1:
        exit(0)
    else:
        exit(1)
