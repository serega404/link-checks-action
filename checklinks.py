import os
import re
import sys
import requests

url_regex = r'https?://[^\s\'"<>)\]\}[^)]+'

def find_links_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.finditer(url_regex, content, re.MULTILINE)
    return [match.group() for match in matches]

def main():
    file_path = os.environ["INPUT_FILEPATH"]
    ignore_codes = os.environ.get("INPUT_IGNORECODES", "")
    ignore_sites = os.environ.get("INPUT_IGNORESITES", "")

    if not file_path:
        if len(sys.argv) != 2:
            print("Usage: python checklinks.py <file_path>")
            sys.exit(1)
        file_path = sys.argv[1]

    if ignore_codes:
        ignore_codes = [int(code.strip()) for code in ignore_codes.split(',')]
    else:
        ignore_codes = []

    if ignore_sites:
        ignore_sites = [site.strip() for site in ignore_sites.split(',')]
    else:
        ignore_sites = []

    print(f"Search for links in a file: {file_path}")
    links = find_links_in_file(file_path)
    if not links:
        print("No links found.")
        sys.exit(0)
    else:
        print(f"Links found: {len(links)}\n")

    site_with_problems = []

    for url in links:
        if any(url.startswith(ignore_site) for ignore_site in ignore_sites):
            print(f"✅ {url} -> 'OK' (ignored site)")
            continue

        try:
            resp = requests.head(url, allow_redirects=True, timeout=5)
        except Exception as e:
            site_with_problems.append(url + " Exception: " + str(e))

        if resp.status_code != 200:
            if resp.status_code in ignore_codes:
                print(f"✅ {url} -> 'OK' (ignored code: {resp.status_code})")
                continue
            site_with_problems.append(url + " Code: " + str(resp.status_code))
            print(f"❌ {url} -> 'FAIL' Code: " + str(resp.status_code))
        else:
            print(f"✅ {url} -> 'OK'")
    
    if site_with_problems:
        print("\nProblematic links:")
        for url in site_with_problems:
            print(f"❌ {url}")
        sys.exit(1)

if __name__ == "__main__":
    main()