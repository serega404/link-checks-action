# Links check action

The script searches for all the links in the file and sends requests to them. If there is a link that does not return code 200, the program will terminate with code 1 after checking all links.

## Usage

```yaml
name: Test links
on:
  - push
  - pull_request

jobs:
  check_urls:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Link check action
        uses: serega404/links-check-action@v0.0.1
        with:
          filePath: "README.md"
          ignoreCodes: "403,418"
          ignoreSites: "https://example.com,http://test.com"
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `filePath`  | Path to the file to check links |
| `ignoreCodes` _(optional)_  | A comma-separated list of HTTP status codes to ignore (e.g., `404,500`) |
| `ignoreSites` _(optional)_  | A comma-separated list of sites to ignore (e.g., `https://example.com,http://test.com`) |

### References

* https://github.com/adriancoman/link-checks-action
* https://github.com/jacobtomlinson/python-container-action

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information.
