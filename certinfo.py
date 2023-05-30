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
        text=True,
        stdin=subprocess.DEVNULL,
    )

    certificates = []
    cert = ""
    for line in result.stdout.splitlines():
        if line == "-----BEGIN CERTIFICATE-----":
            cert = ""
        cert += f"{line}\n"
        if line == "-----END CERTIFICATE-----":
            certificates.append(cert)

    return certificates


def print_cert_info(cert):
    result = subprocess.run(
        ["openssl", "x509", "--subject", "--noout"],
        capture_output=True,
        text=True,
        input=cert,
    )

    print(result.stdout)


def main():
    certs = get_remote_certificates("google.de")
    for c in certs:
        print_cert_info(c)


if __name__ == "__main__":
    main()
