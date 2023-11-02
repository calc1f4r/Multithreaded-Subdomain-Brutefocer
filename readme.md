### Multithreaded Network Scanner

SubBuster is a Python tool designed for brute-forcing subdomain enumeration. It enables users to explore and validate potential subdomains for a particular target domain.



https://github.com/calc1f4r/Multithreaded-Subdomain-Brutefocer/assets/74751675/c5d0a2f7-b2f3-41a2-934a-f0e6794f7278



#### Features

- Subdomain enumeration for target domains.
- Customizable scanning options.
- Status code and response size matching.
- Multi-threaded scanning for speed.
- Save results to an output file.
- User-Agent customization.
- Display response titles.
- Exception handling for robust performance.

#### Usage

- Clone the repository to your local machine.

```bash
git clone https://github.com/yourusername/your-repo.git
```

- Change into the project directory.

```bash
cd SUBDOMAIN
```

- Install the required Python packages using pip.

```bash
pip install -r requirements.txt
```

- Run the Subdomain Bruteforcer by providing the target domain and other optional parameters.

```bash
python subBrute.py -d example.com -t 20 -r -H "Header1: val1" -H "Header2: val2" -mc 200 301 404 -ms 1024 2048 -fc 500 503 -fs 4096 8192 -w wordlist.txt -o results.txt
```

###### Various other Options

- `-d` or `--domain`: Specify the target domain to scan.
- `-t` or `-threads`: Set the number of threads for parallel scanning.
- `-r` or `--follow-redirect`: Follow HTTP redirects.
- `-H` or `--headers`: Customize HTTP headers with key-value pairs.
- `-mc` or `--match-codes`: Include status codes to match (e.g., 200 301).
- `-ms` or `--match-size`: Match response size (e.g., 1024 2048).
- `-fc` or `--filter-codes`: Filter out specific status codes.
- `-fs` or `--filter-size`: Filter specific response sizes.
- `-w` or `--wordlist`: Specify the wordlist file for subdomain enumeration.
- `-o` or `--output`: Save results to an output file
