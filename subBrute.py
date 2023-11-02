import argparse
import requests
from threading import Thread
from queue import Queue
from bs4 import BeautifulSoup
from termcolor import colored
from os import path
from sys import exit
from datetime import datetime

def get_args():
    parser=argparse.ArgumentParser()
    
    parser.add_argument('-d','--domain',dest="target",help="Domain to scan ",required=True)
    parser.add_argument('-t','-threads',dest="threads",help="Specify the threads, (Default => 10)",type=int,default=10)

    parser.add_argument('-r', '--follow-redirect', dest="follow_redirect", action='store_true',
                        help="Follow redirects")

    
    parser.add_argument('-H', '--headers', dest="header", nargs='*',help="Specify HTTP headers (e.g., -H 'Header1: val1' -H 'Header2: val2')")
    
    parser.add_argument('-a', '--useragent', metavar='string', dest="user_agent",default="SubBuster/1.0", help="Set the User-Agent string (default 'SubBuster/1.0')")
        
    parser.add_argument('--ignore-code',dest='ignore_codes',type=int,help="Codes to ignore",nargs='*')
    
    parser.add_argument('-ht', '--hide-title', dest="hide_title", action='store_true',help="Hide response title in output")
    
    parser.add_argument('-mc', dest='match_codes', nargs='*',
                        help="Include status codes to match, separated by space (e.g., -mc 200 404)")

    parser.add_argument('-ms', dest='match_size', nargs='*',
                        help="Match response size, separated by space")

    parser.add_argument('-fc', dest="filter_codes", nargs='*',help="Filter status codes, separated by space")

    parser.add_argument('-fs', nargs='*', dest='filter_size',
                        help="Filter response size, separated by space")
    
    parser.add_argument('-w','--wordlist',dest='wordlist',required=False,default='wordlist.txt',help="Specify the wordlist to use !")
    
    
    parser.add_argument('-o', '--output', dest='output',
                        help="Path to the output file to save results")
    
    try:
        return parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        exit(1)

class SubdomainBruteforcer:
    def __init__(self, target, wordlist, follow_redirect, headers, match_codes, match_size, filter_codes, filter_size, hide_title, threads):
        self.target = target
        self.wordlist = wordlist
        self.follow_redirect = follow_redirect
        self.headers = headers
        self.hide_title = hide_title
        self.match_codes = match_codes
        self.match_size = match_size
        self.filter_codes = filter_codes
        self.filter_size = filter_size
        self.threads = threads
        self.q = Queue()
        self.subdomains = []

    def main(self):
        # Start threads to process subdomains
        for _ in range(self.threads):
            thread = Thread(target=self.get_subdomain)
            thread.daemon = True
            thread.start()

        # Read subdomains from the wordlist and put them into the queue
        with open(self.wordlist, 'r') as f:
            self.subdomains.extend(f.read().strip().splitlines())

        for subdomain in self.subdomains:
            self.q.put(subdomain)
        self.q.join()

    def get_subdomain(self):
        while True:
            subdomain = self.q.get()
            self.sub_brute(subdomain)
            self.q.task_done()

    def sub_brute(self, subdomain):
        # Function to handle subdomains
        try:
            url = f"https://{subdomain}.{self.target}"
            response = self.make_request(url)
        except:
            pass
        else:
            response_length = len(response.text)
            status_code = response.status_code
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else []

            if self.is_match(status_code, response_length):
                self.print_data(status_code, response_length, url, title)

    def make_request(self, url):
        session = requests.Session()
        session.headers.update(self.headers)
        response = session.get(url, allow_redirects=self.follow_redirect, timeout=1)
        return response

    def is_match(self, status_code, response_length):
        status_code = str(status_code)
        response_length = str(response_length)
        

        if self.match_codes:
            if status_code not in self.match_codes:
                return False

        if self.filter_codes and status_code in self.filter_codes:
            return False

        if self.match_size:
            if response_length not in self.match_size:
                return False

        if self.filter_size and response_length in self.filter_size:
            return False

        return True

    def print_data(self, status_code, response_length, url, title):
        status_code = int(status_code)
        color = 'grey'
        if 200 <= status_code < 300:
            color = 'green'
        elif 300 <= status_code < 400:
            color = 'yellow'
        elif 400 <= status_code < 500:
            color = 'red'
        elif 500 < status_code < 600:
            color = 'magenta'

        status_code_str = str(status_code).ljust(9, " ")
        response_length_str = str(response_length).ljust(9)
        url_str = url.ljust(30)

        output = f"{colored(status_code_str, color)} {response_length_str} {url_str}"

        if not self.hide_title:
            output += f" [{title}]"

        print(output)

    def print_banner(self):
        print("-" * 80)
        print(colored(
            f"Subdomain Bruteforcing starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'cyan', attrs=['dark']))
        print("-" * 80)
        print(colored("[*] Target Domain".ljust(20, " "),
                      'light_red'), ":", f"{self.target}")
        print(colored("[*] Wordlist".ljust(20, " "),
                      'light_red'), ":", f"{self.wordlist}")
        if self.headers:
            print(colored("[*] Headers".ljust(20, " "),
                          'light_red'), ":", f"{self.headers}")
        if self.match_size:
            print(colored("[*] Match Res size".ljust(20, " "), 'light_red'),
                  ":", f"{self.match_size}")
        if self.threads:
            print(colored("[*] Threads".ljust(20, " "), 'light_red'),
                  ":", f"{self.threads}")
        if self.match_codes or self.filter_codes:
            if self.match_codes:
                print(colored("[*] Match Codes".ljust(20, " "),
                              'light_red'), ":", f"{self.match_codes}")

            if self.filter_codes:
                print(colored("[*] Filter Codes".ljust(20, " "), 'light_red'),
                      ":", f"{self.filter_codes}")
        else:
            print(colored("[*] Status Codes".ljust(20, " "),
                          'light_red'), ":", f"All Status Codes")

        if self.filter_size:
            print(colored("[*] Filter Response Size".ljust(20, " "), 'light_red'),
                  ":", f"{self.filter_size}")
        print("-" * 80)
        print("-" * 80)

if __name__ == "__main__":
    arguments = get_args()
    target = arguments.target
    hide_title = arguments.hide_title or False
    redirection = arguments.follow_redirect or False
    user_agent = arguments.user_agent
    match_codes = arguments.match_codes
    match_size = arguments.match_size
    filter_codes = arguments.filter_codes
    filter_size = arguments.filter_size
    header = arguments.header
    wordlist = arguments.wordlist
    threads = arguments.threads

    if match_size and filter_size:
        print(colored(
            "[+] For now, using Matching and Filtering Response Length together is not available!", 'red'))
        exit()
    if match_codes and filter_codes:
        print(colored(
            "[+] For now, using Matching and Filtering Response Status code together is not available!", 'red'))
        exit()
    if not path.exists(wordlist):
        print(colored("[-] Provide a valid wordlist file!", 'red'))
        exit()

    headers = {}
    if header:
        for h in header:
            key, value = h.split(':', 1)
            headers[key] = value.strip()
    headers['User-Agent'] = user_agent

    bruteforcer = SubdomainBruteforcer(target, wordlist, redirection, headers, match_codes, match_size, filter_codes, filter_size, hide_title, threads)
    bruteforcer.print_banner()
    bruteforcer.main()
