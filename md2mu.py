from mistune import Markdown
import argparse
import re
from underlined import underlined
from micron import MicronRenderer

def main():

    parser = argparse.ArgumentParser(description="Converts a Markdown file to Micron format")
    parser.add_argument("md_file", nargs="?", default=None, help="Markdown formatted source file", type=str)
    parser.add_argument("mu_file", nargs="?", default=None, help="Micron formatted destination file", type=str)
    parser.print_usage = parser.print_help
    args = parser.parse_args()

    with open(args.md_file, 'r') as mdf:
        md_str = mdf.read()
    
    m2μr = MicronRenderer()
    m2μ = Markdown(renderer=m2μr)
    underlined(m2μ)

    with open(args.mu_file, 'w') as muf:
        md_str = muf.write(m2μ(md_str))

if __name__ == "__main__":
	main()