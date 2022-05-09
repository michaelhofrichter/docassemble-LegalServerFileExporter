# LegalServer File Exporter
This package can be used to download all the documents associated with a LegalServer Case/Matter.

## Docassemble Server Setup
In your configuration file, you will need to store your login information for a LegalServer API call. The format should be as follows:
```
legalserver:
  site_name:
    username: username
    password: password
```
Where `site_name` is the legalserver site abbreviation (like `demo4-demo`) and the username/password are for an account that has Reports API access. Specifically, the `Login`, `API Access`, and `API Basic Case Information` permissions are needed. 

## Change Log
* 0.0.1 - Initial MVP
