# CFDNS
Quick and dirty™ Python script to edit clients' DNS records using the [Cloudflare Hosting Provider API](https://www.cloudflare.com/docs/host-api/) that I made after getting tired of using chained Curl requests every time I was asked for support. As I was the only intended user and the goal was to save time many inputs aren't properly escaped and printed strings aren't formatted. If you'd like to improve it feel free to fork and issue pull requests.

## Usage
```
$ ./cfdns.py
API key: 0123456789abcdef0123456789abcdef
Client Email: client@example.org

#	Status		Zone
-----------------------------------------
0	active		example.org
1	active		example.net
2	active		example.com

B	(back)
X	(exit)

Zone #: 2

Selected Zone: example.com
Name Servers: example.ns.cloudflare.com example2.ns.cloudflare.com

#	Record			Type	Content		Proxied	TTL
---------------------------------------------------------------
0	example.com	A	192.0.2.1	True	1
1	mail.example.com	A	192.0.2.2	False	1
2	www.example.com	CNAME	example.com	False	1
3	example.com	MX	mail.example.com	False	3600

Options:
N	(new)
E	(edit)
D	(delete)
B	(back)
X	(exit)

Option: N
Type (A, AAAA, CNAME, TXT, SRV...): TXT
Name: example.com
Content: v=spf1 ip4:192.0.2.2 -all
TTL: 
Priority: 
Proxied (True/False): False

Record:

content: v=spf1 ip4:192.0.2.2 -all
proxied: False
type: TXT
name: example.com
OK? (Y/N/B/X): Y

#	Record			Type	Content		Proxied	TTL
---------------------------------------------------------------
0	example.com	A	192.0.2.1	True	1
1	mail.example.com	A	192.0.2.2	False	1
2	www.example.com	CNAME	example.com	False	1
3	example.com	MX	mail.example.com	False	3600
4	example.com TXT	v=spf1 ip4:192.0.2.2 -all	False	1

Options:
N	(new)
E	(edit)
D	(delete)
B	(back)
X	(exit)

Option: X
$ 
```
