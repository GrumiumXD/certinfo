#!/usr/bin/env python3

import argparse
import subprocess


def filter_certificate_list():
    pass


def get_remote_certificates(host_name, port=443):
    result = subprocess.run(
        [
            "openssl",
            "s_client",
            "--connect",
            f"{host_name}:{port}",
            "--servername",
            f"{host_name}",
            "--showcerts",
        ],
        capture_output=True,
        stdin=subprocess.DEVNULL,
    )

    print(result.stdout)


def main():
    get_remote_certificates("google.de")


if __name__ == "__main__":
    main()
