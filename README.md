# md2mu

Simple CLI tool to convert existing Markdown files into Micron format to use in [Nomad Network](https://github.com/markqvist/NomadNet) nodes

```
usage: md2mu.py [-h] [md_file] [mu_file]

Converts a Markdown file to Micron format

positional arguments:
  md_file     Markdown formatted source file
  mu_file     Micron formatted destination file

options:
  -h, --help  show this help message and exit
```

## Usage:

```
$ python3 md2mu.py markdown.md micron.mu
```