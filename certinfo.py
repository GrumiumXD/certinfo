#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path



def get_certificate_chunks(certificate_string):
    certificates = []
    cert = ""
    for line in certificate_string.splitlines():
        if line == "-----BEGIN CERTIFICATE-----":
            cert = ""
        cert += f"{line}\n"
        if line == "-----END CERTIFICATE-----":
            certificates.append(cert)

    return certificates


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

    return get_certificate_chunks(result.stdout)


def get_file_certificates(path):
    txt = Path(path).read_text()
    return get_certificate_chunks(txt)


def print_cert_info_text(cert):
    result = subprocess.run(
        ["openssl", "x509", "--text", "--noout"],
        capture_output=True,
        text=True,
        input=cert,
    )

    print(result.stdout)

def print_issuer_info(cert):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", choices=["text", "pem", "issuer"], default="text"
    )

    subparsers = parser.add_subparsers(required=True, dest="option")

    remote_parser = subparsers.add_parser("remote")
    remote_parser.add_argument("host")
    remote_parser.add_argument("-p", "--port", default=443, type=int)

    file_parser = subparsers.add_parser("file")
    file_parser.add_argument("path")

    args = parser.parse_args()
    print(args)

    certificates = []
    if args.option == "remote":
        certificates = get_remote_certificates(args.host, args.port)
    else:
        certificates = get_file_certificates(args.path)

    for c in certificates:
        if args.output == "text":
            print_cert_info_text(c)
        elif args.output == "issuer":
            print_issuer_info(c)
        else:
            print(c)
    # certs = get_remote_certificates("google.de")
    # for c in certs:
    #     print_cert_info(c)


if __name__ == "__main__":
    main()
