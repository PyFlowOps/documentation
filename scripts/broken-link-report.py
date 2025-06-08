import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import colorama
from colorama import Fore, Style
import argparse
import time
import yaml

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
        self.link_sources = {}  # Track where each link was found

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
                    # Extract the HTML context around the link
                    parent_element = a_tag.parent
                    html_context = str(parent_element)[:200] + "..." if len(str(parent_element)) > 200 else str(parent_element)
                    
                    # Store the source information
                    if absolute_url not in self.link_sources:
                        self.link_sources[absolute_url] = []
                    self.link_sources[absolute_url].append({
                        'source_url': url,
                        'anchor_text': a_tag.text.strip() or "[No anchor text]",
                        'html_context': html_context
                    })
                    
                    links.append(absolute_url)
            
            return links
        except Exception as e:
            print(f"{Fore.RED}Error extracting links from {url}: {e}")
            return []

    def crawl(self):
        """Start crawling from the base URL"""
        urls_to_visit = [self.base_url]
        
        print(f"{Fore.CYAN}Starting link check on {self.base_url}")
        print(f"{Fore.CYAN}Checking external links: {self.check_external}")
        
        while urls_to_visit:
            current_url = urls_to_visit.pop(0)
            
            # Skip if already visited
            if current_url in self.visited_urls:
                continue
                
            print(f"{Fore.YELLOW}Checking: {current_url}")
            
            # Add to visited set
            self.visited_urls.add(current_url)
            
            # Check if the link works
            is_working, status = self.check_link(current_url)
            if not is_working:
                self.broken_links.append((current_url, status))
                print(f"{Fore.RED}Broken link: {current_url} (Status: {status})")
                continue
                
            # Only crawl pages from our domain
            if urlparse(current_url).netloc != self.domain:
                continue
                
            # Extract links from the page
            links = self.extract_links(current_url)
            for link_url in links:
                if link_url not in self.visited_urls:
                    urls_to_visit.append(link_url)
            
            # Add a delay to avoid overwhelming the server
            if self.delay > 0:
                time.sleep(self.delay)
                
        return self.broken_links

def main():
    parser = argparse.ArgumentParser(description='Check for broken links on a website')
    parser.add_argument('url', help='The base URL to start scanning from')
    parser.add_argument('--external', action='store_true', help='Also check external links')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between requests in seconds')
    parser.add_argument('--output', help='Save results to a file')
    args = parser.parse_args()
    
    checker = LinkChecker(args.url, external=args.external, delay=args.delay)
    broken_links = checker.crawl()
    
    # Report results
    print("\n" + "="*80)
    print(f"{Fore.CYAN}Link Check Summary:")
    print(f"Total URLs checked: {len(checker.visited_urls)}")
    print(f"Broken links found: {len(broken_links)}")
    
    # Prepare output text for file if needed
    output_text = []
    output_text.append(f"Link Check Summary:")
    output_text.append(f"Total URLs checked: {len(checker.visited_urls)}")
    output_text.append(f"Broken links found: {len(broken_links)}")
    
    if broken_links:
        print("\n" + "="*80)
        print(f"{Fore.RED}List of broken links:")
        output_text.append("\nList of broken links:")
        
        for url, status in broken_links:
            # Get the sources for this broken link
            sources = checker.link_sources.get(url, [])
            
            print(f"{Fore.RED}URL: {url}")
            print(f"{Fore.YELLOW}Status/Error: {status}")
            output_text.append(f"\nURL: {url}")
            output_text.append(f"Status/Error: {status}")
            
            print(f"{Fore.GREEN}Found in {len(sources)} location(s):")
            output_text.append(f"Found in {len(sources)} location(s):")
            
            for idx, source_info in enumerate(sources, 1):
                print(f"{Fore.CYAN}  {idx}. Page: {source_info['source_url']}")
                print(f"{Fore.CYAN}     Anchor text: {source_info['anchor_text']}")
                print(f"{Fore.CYAN}     HTML context: {source_info['html_context']}")
                
                output_text.append(f"  {idx}. Page: {source_info['source_url']}")
                output_text.append(f"     Anchor text: {source_info['anchor_text']}")
                output_text.append(f"     HTML context: {source_info['html_context']}")
            
            print("-"*80)
            output_text.append("-"*80)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_text))
        print(f"{Fore.GREEN}Results saved to {args.output}")
        
    print(f"{Fore.GREEN}Link check completed!")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear') # Clear the console

    # Run the main function
    main()
