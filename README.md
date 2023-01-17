### How to Use
Use Python 3.9

Here are some sample commands you can try:
```
python DnsClient.py -t 10 -r 2 -mx @8.8.8.8 mcgill.ca
python DnsClient.py -t 10 -r 2 -ns @8.8.8.8 fr.wiktionary.org
python DnsClient.py -t 10 -r 2 -mx @8.8.8.8 gmail.com
python DnsClient.py -t 10 -r 2 -mx @8.8.8.8 mail.google.com
python DnsClient.py -t 10 -r 2 -ns @8.8.8.8 www.amazon.com
python DnsClient.py -t 1 -r 2 @8.8.8.8 www.mypokemonteam.com
python DnsClient.py -mx @8.8.8.8 pokemonshowdown.com
python DnsClient.py @8.8.8.8 -ns google.com.hk
python DnsClient.py @1.1.1.1 -ns google.com.hk
```

Commands that will fail due to improper arguments:
```
python DnsClient.py
python DnsClient.py -t 10 -r 2 -mx @8.8.8.8
python DnsClient.py -t 10 -r 2 -mx 8.8.8.8 mcgill.ca
python DnsClient.py -r 0.5 -mx 8.8.8.8 mcgill.ca
python DnsClient.py -mx -ns 8.8.8.8 mcgill.ca
python DnsClient.py -mx 3 8.8.8.8 mcgill.ca
python DnsClient.py -t 0 -mx @8.8.8.8 mcgill.ca
python DnsClient.py -r "-3" -mx @8.8.8.8 mcgill.ca
```

Commands that will cause socket-related errors (assuming the address does not handle DNS requests):
```
python DnsClient.py -t 3 -r 2 -mx @127.0.0.1 mcgill.ca
```

RCODE=3 NOT FOUND result:
```
python DnsClient.py @8.8.8.8 -ns www.google.com.hk
```

Getting additional records (needs McGill VPN):
```
python DnsClient.py @132.206.85.18 ece.mcgill.ca -ns
```

### Test
- [x] A
- [x] NS
- [x] CNAME
- [x] MX
- [x] mcgill.ca
- [x] www.google.com
- [x] www.amazon.com
- [x] pokemonshowdown.com
- [x] mypokemonteam.com
- [x] argument failures
- [x] max retries failure
- [x] two more website addresses to test
- [x] Response with additional section
- [ ] ~~Response with authority and additional section~~ (probably not necessary)
- [ ] ~~all the different RCODE failures~~ (TA said focus more on incorrect inputs from users)