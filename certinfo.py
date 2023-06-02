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
        ["openssl", "x509", "--text", "--nameopt", "multiline", "--noout"],
        capture_output=True,
        text=True,
        input=cert,
    )

    print(result.stdout)


def print_issuer_info(cert):
    subject_hash = subprocess.run(
        ["openssl", "x509", "--subject_hash", "--noout"],
        capture_output=True,
        text=True,
        input=cert,
    ).stdout.strip()

    issuer_hash = subprocess.run(
        ["openssl", "x509", "--issuer_hash", "--noout"],
        capture_output=True,
        text=True,
        input=cert,
    ).stdout.strip()

    subject = subprocess.run(
        ["openssl", "x509", "--subject", "--nameopt", "dn_rev", "--noout"],
        capture_output=True,
        text=True,
        input=cert,
    ).stdout.strip()
    subject = subject.lstrip("subject=")

    issuer = subprocess.run(
        ["openssl", "x509", "--issuer", "--nameopt", "dn_rev", "--noout"],
        capture_output=True,
        text=True,
        input=cert,
    ).stdout.strip()
    issuer = issuer.lstrip("issuer=")

    print(f"S: {subject_hash} ({subject})\n\t|\n\tV\nI: {issuer_hash} ({issuer})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        choices=["text", "pem", "issuer"],
        default="text",
        help="what information to display",
    )

    subparsers = parser.add_subparsers(
        required=True, dest="subcommand", title="sub commands"
    )

    remote_parser = subparsers.add_parser(
        "remote", help="fetch and display certificate(s) from a remote server"
    )
    remote_parser.add_argument("host", help="host name for the remote server")
    remote_parser.add_argument(
        "-p", "--port", default=443, type=int, help="port for the remote service"
    )

    file_parser = subparsers.add_parser(
        "file", help="fetch and display certificate(s) from a local file"
    )
    file_parser.add_argument("path", help="path to the certificate file")

    args = parser.parse_args()

    certificates = (
        get_remote_certificates(args.host, args.port)
        if args.subcommand == "remote"
        else get_file_certificates(args.path)
    )

    for c in certificates:
        if args.output == "text":
            print_cert_info_text(c)
        elif args.output == "issuer":
            print_issuer_info(c)
        else:
            print(c)


if __name__ == "__main__":
    main()
