# check_mailserverprotection

Checks the following email-related attributes for a provided domain:
- Mail Servers (MX Records)
- SPF record
- DMARC record
- DKIM record
- DKIM Encryption level

### DKIM Record Lookup:
The script checks if the mail servers are Google Workspace or Microsoft 365 and uses the default records for those services.
If the mail servers are not Google Workspace or Microsoft 365, the Selector will need to be provided. The Selector is included in the email headers, typically in the DKIM-Signature. 

Example of DKIM-Signature:
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=github.com; s=google;
The "s" in "s=google" stands for the Selector, which in this case is "google."

## Legal Disclaimer:
You, the executor, runner, or user, accept all liability.
This code comes with ABSOLUTELY NO WARRANTY.
You may redistribute copies of the code under the terms of the GPL v3.

## Background:
This script was created to streamline email server-related checks for assessments and reconnaissance.

## Instructions:
- Download `check_mail_server_protection.py`
- Run the script using Python:
  ```bash
  python check_mail_server_protection.py --domain github.com
  python check_mail_server_protection.py --domain github.com --selector google
