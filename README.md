# crt.sh Domain Finder

Get all the related domains and subdomains using [crt.sh](https://crt.sh/).

## Installation

To install dependencies, use the following command:

```bash
pip3 install -r requirements.txt
```

## Using the crt.sh Domain Finder

To run the crt.sh Domain Finder on a domain, use the '-d' flag and provide the domain as an argument:

```bash
python crt_sh_domains.py -d example.com
```

For an overview of all commands use the following command:

```bash
python3 crt_sh_domains.py -h
```

The output shown below are the latest supported commands.

```bash
usage: crt_sh_domains.py [-h] -d DOMAIN [-o OUTPUT]

Get domains from crt.sh

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain to search for domains
  -o OUTPUT, --output OUTPUT
                        Output file to write domains to

Example: python crt_sh_domains.py -d example.com -o domains.txt
```

**NOTE:** Do check out **[Golang Version of crt.sh Domain Finder](https://github.com/shivamsaraswat/crt_sh_go)**.
