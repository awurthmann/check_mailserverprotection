# check_mailserverprotection

Based on and converted from the PowerShell script with the same name.

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
- Download `check_mail_server.py`
- Run the script using Python:
  ```bash
  python check_mail_server.py --domain github.com
  python check_mail_server.py --domain github.com --selector google
  ```
- Example Output:
  ```bash
  
  Domain: github.com
  MailServers: ['aspmx.l.google.com.', 'alt3.aspmx.l.google.com.', 'alt4.aspmx.l.google.com.', 'alt1.aspmx.l.google.com.', 'alt2.aspmx.l.google.com.']
  SPF: v=spf1 ip4:192.30.252.0/22 include:_netblocks.google.com include:_netblocks2.google.com include:_netblocks3.google.com include:spf.protection.outlook.com include:mail.zendesk.com include:_spf.salesforce.com include:servers.mcsv.net ip4:166.78.69.169 ip4:1" "66.78.69.170 ip4:166.78.71.131 ip4:167.89.101.2 ip4:167.89.101.192/28 ip4:192.254.112.60 ip4:192.254.112.98/31 ip4:192.254.113.10 ip4:192.254.113.101 ip4:192.254.114.176 ip4:62.253.227.114 ~all
  DMARC: ['v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@github.com']
  DKIM: ['v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAj6T5sl/RwdSqGoYWaWaFbS2UAeyPrEmd0gogocmRfS441qwR8/0KB81Hw89P0l4YiFRrXYk7NVIGfyCRHAYYZUzCkGeOysI2EjgzLFhd/NEsbRzOEc/kWkK/RO6JFq/5lOn6M9AZw/ap9tds4JG9ApgNNdSpPxp9DmvpsOSgNMVflRxQFrk3kdS4RNAPKu/OP" "oA7dlR/A/pECryjRoYgENtDXzdnK70HgCekems6UDzxDj61cjyoKoXtEMF/QsaHEQ1Gjfv014rDJBsubk/kT5VqHkWHa/ia68Z5r228Ety/wFfQNjXTx/J7KGZ9GkZlKED659eiJcLnWcKDSiQlhwIDAQAB']
  DKIM Encryption: 2048
  ```
## Note
Technically the mail server isn't being checked, DNS records related to the mail environment are being checked. This script should probably be named mail_oint or check_mail_records. I originally planned to add port probes to the script but have since changed my mind.
