# Setup
install the dependencies
```
pip install -r requirements.txt
```
Also create an `.env` file with following content:
```dotenv
CLOUDFLARE_API_TOKEN=
CLOUDFLARE_ZONE_ID=
CLOUDFLARE_DNS_RECORD_ID=
DOMAIN=
```

where `CLOUDFLARE_API_TOKEN` is your API token that is generated at the account level from cloudflare

ZONE_ID can be extracted from cloudflare by clicking on a domain in the dashboard, going to overview tab and scroll down and check on the right side

DNS_RECORD_ID is the id for the DNS record that we want to update. This can be automated but for now I have kept it in env file. 
To get the DNS record ID, run following URL and get the ID for the record you want to update
```
curl --location 'https://api.cloudflare.com/client/v4/zones/{ZONE_ID_HERE}/dns_records?type=A' \
--header 'Authorization: Bearer {TOKEN_HERE}'
```