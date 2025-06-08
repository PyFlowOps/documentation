import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import colorama
from colorama import Fore, Style
import argparse
import yaml
import time
 
from halo import Halo
from icecream import ic

# Initialize colorama for colored terminal output
colorama.init(autoreset=True)

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "config.yml"), "r") as f:
    exclusions = yaml.safe_load(f)["exclude"]

class LinkChecker:
    def __init__(self, base_url, external=False, delay=0):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.broken_links = []
        self.check_external = external
        self.delay = delay

    def is_valid_url(self, url):
        """Check if URL is valid and belongs to the same domain (if external=False)"""
        parsed = urlparse(url)
        
        # Skip mailto, tel, javascript, etc.
        if parsed.scheme and parsed.scheme not in ['http', 'https']:
            return False
            
        # Check if we should only scan internal links
        if not self.check_external and parsed.netloc and parsed.netloc != self.domain:
            return False
            
        return True

    def check_link(self, url):
        """Check if a link is working by sending a HEAD request"""
        for i in exclusions:
            if i in url:
                return True, 301

        try:
            response = requests.head(url, allow_redirects=True, timeout=10)

            if response.status_code >= 400:
                # Try with GET if HEAD doesn't work (some servers don't support HEAD)
                response = requests.get(url, timeout=10, stream=True)
                response.close()  # Close connection without downloading the whole content
            
            if response.status_code >= 400:
                return False, response.status_code
            return True, response.status_code
        except requests.exceptions.RequestException as e:
            return False, str(e)

    def extract_links(self, url):
        """Extract all links from a given URL"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code >= 400:
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            # Extract links from anchor tags
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                absolute_url = urljoin(url, href)
                if self.is_valid_url(absolute_url):
                    links.append((absolute_url, a_tag.text.strip() or "[No anchor text]"))
            
            return links
        except Exception as e:
            Halo(f"{Fore.RED}Error extracting links from {url}: {e}").fail()
            return []

    def crawl(self):
        """Start crawling from the base URL"""
        urls_to_visit = [(self.base_url, "Starting page")]
        
        print(f"{Fore.CYAN}Starting link check on {self.base_url}")
        print(f"{Fore.CYAN}Checking external links: {self.check_external}")
        
        with Halo(text="Checking for broken links...", spinner='dots') as spinner:
            while urls_to_visit:
                current_url, source_text = urls_to_visit.pop(0)
                
                # Skip if already visited
                if current_url in self.visited_urls:
                    continue
                
                ic(f"{Fore.YELLOW}Checking: {current_url}")
                
                # Add to visited set
                self.visited_urls.add(current_url)
                
                # Check if the link works
                is_working, status = self.check_link(current_url)
                
                if not is_working:
                    if current_url.endswith('index.md'):
                        # Let's break the index.md part off and check that link
                        _curl = current_url.rstrip('index.md')
                        _isw, _stat = self.check_link(_curl)
                        if _isw and _stat == 200:
                            continue

                    if current_url.endswith('readme.md'):
                        # Let's break the readme.md part off and check that link
                        _curl = current_url.rstrip('readme.md')
                        _isw, _stat = self.check_link(_curl)
                        if _isw and _stat == 200:
                            continue

                    self.broken_links.append((current_url, status, source_text))
                    spinner.fail(f"{Fore.RED}⛔ Broken link: {current_url} (Status: {status}) ⛔")
                    spinner.info(f"Broken link found in: {source_text}")
                    continue
                    
                # Only crawl pages from our domain
                if urlparse(current_url).netloc != self.domain:
                    continue
                    
                # Extract links from the page
                links = self.extract_links(current_url)
                for link_url, anchor_text in links:
                    if link_url not in self.visited_urls:
                        urls_to_visit.append((link_url, anchor_text))
                
                # Add a delay to avoid overwhelming the server
                if self.delay > 0:
                    time.sleep(self.delay)
                
                if globals().get('verbose'):
                    spinner.succeed(f"{Fore.GREEN}✅ Working link: {current_url} (Status: {status})")
                    
            return self.broken_links


def main():

    parser = argparse.ArgumentParser(description='Check for broken links on a website')
    parser.add_argument('url', help='The base URL to start scanning from')
    parser.add_argument('--external', action='store_true', help='Also check external links')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between requests in seconds')
    parser.add_argument('--debug', default=False, action='store_true', help='Enable debug mode')
    parser.add_argument('--verbose', default=False, action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    global verbose
    verbose = args.verbose
    ic.disable() # Disable icecream by default

    if args.debug:
        ic.configureOutput(includeContext=True)
        ic.enable()
        print(f"{Fore.YELLOW}Debug mode enabled")

    checker = LinkChecker(args.url, external=args.external, delay=args.delay)
    broken_links = checker.crawl()
    
    # Report results
    print("\n" + "="*80)
    print(f"{Fore.CYAN}Link Check Summary:")

    print(f"Total URLs checked: {len(checker.visited_urls)}")
    print(f"Broken links found: {len(broken_links)}")
    print("\n" + "="*80)
    if broken_links:
        Halo(f"{Fore.RED}Broken links found: {len(broken_links)} 🚨").fail()

        print("\n" + "="*80)
        print(f"{Fore.RED}List of broken links:")
        for url, status, source in broken_links:
            print(f"{Fore.RED}URL: {url}")
            print(f"{Fore.YELLOW}Status/Error: {status}")
            print(f"{Fore.YELLOW}Found in: {source}")
            print("-"*80)
    else:
        Halo(text=f"{Fore.GREEN}No broken links found! 🏆", spinner='dots').succeed()
        
    Halo(f"{Fore.RESET}Link check completed!").info()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear') # Clear the console
    
    main() # This is the main function that starts the script
