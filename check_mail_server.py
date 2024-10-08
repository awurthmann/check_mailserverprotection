#!/usr/bin/env python3

# Written by: Aaron Wurthmann
#
# You the executor, runner, user accept all liability.
# This code comes with ABSOLUTELY NO WARRANTY.
#
# ----------------------------------------------------------------------------------------------------------
# Name: check_mail_server.py
# Version: 2024.10.07.0950
# Description: Checks the following email-related attributes for a provided domain:
#               Mail Servers (MX Records), SPF record, DMARC record, DKIM record, DKIM Encryption level.
#               This script automatically detects DKIM selectors for Google Workspace and Microsoft 365.
#               If the mail servers are not Google or Microsoft, a DKIM selector must be provided by the user.
#               DKIM selectors can be found in email headers in the DKIM-Signature field.
#
# Tested with: macOS 14.5 - Python 3.9.0
# ----------------------------------------------------------------------------------------------------------


import dns.resolver
import argparse

def resolve_mx(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return [r.exchange.to_text().lower() for r in answers]
    except Exception as e:
        return f"Error resolving MX records: {e}"

def resolve_txt(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for r in answers:
            txt_record = r.to_text().strip('"')
            if record_type in txt_record.lower():
                return txt_record
        return f"{record_type.upper()} record not found."
    except Exception as e:
        return f"Error resolving {record_type.upper()} record: {e}"

def resolve_dmarc(domain):
    try:
        dmarc_domain = f'_dmarc.{domain}'
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        return [r.to_text().strip('"') for r in answers]
    except Exception as e:
        return f"Error resolving DMARC record: {e}"

def resolve_dkim(domain, selector=None):
    if not selector:
        mx_records = resolve_mx(domain)
        if any("google.com" in mx for mx in mx_records):
            selector = "google"
        elif any("outlook.com" in mx or "onmicrosoft.com" in mx for mx in mx_records):
            selector = "selector1"
            dkim = check_dkim(selector, domain)
            if "not found" in dkim.lower():
                selector = "selector2"
    return check_dkim(selector, domain)

def check_dkim(selector, domain):
    try:
        dkim_domain = f"{selector}._domainkey.{domain}"
        answers = dns.resolver.resolve(dkim_domain, 'TXT')
        return [r.to_text().strip('"') for r in answers]
    except Exception as e:
        return f"DKIM record not found for selector '{selector}': {e}"


def evaluate_dkim_encryption(dkim_record):
    if not dkim_record:
        return "Unknown"

    # Look for the part that starts with 'p=', which contains the public key
    for part in dkim_record:
        if 'p=' in part:
            public_key = part.split('p=')[1]
            key_length = len(public_key)

            # Base64 encoded keys expand the size of the key, so we compare against expected Base64 lengths
            if key_length >= 684:  # 4096-bit key
                return 4096
            elif key_length >= 512:  # 3072-bit key
                return 3072
            elif key_length >= 342:  # 2048-bit key
                return 2048
            elif key_length >= 170:  # 1024-bit key
                return 1024
            else:
                return "Unknown"

    return "Unknown"


def main():
    parser = argparse.ArgumentParser(description="Check Mail Server Protection")
    parser.add_argument('--domain', required=True, help="Domain to check")
    parser.add_argument('--selector', help="DKIM Selector (optional)")
    
    args = parser.parse_args()
    domain = args.domain
    selector = args.selector

    mx_records = resolve_mx(domain)
    spf_record = resolve_txt(domain, 'spf')
    dmarc_record = resolve_dmarc(domain)
    dkim_record = resolve_dkim(domain, selector)
    dkim_encryption = evaluate_dkim_encryption(dkim_record)

    report = {
        'Domain': domain,
        'MailServers': mx_records,
        'SPF': spf_record,
        'DMARC': dmarc_record,
        'DKIM': dkim_record,
        'DKIM Encryption': dkim_encryption
    }

    for key, value in report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
