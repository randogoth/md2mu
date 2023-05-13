import mistune
import argparse

class Markdown2Micron(mistune.HTMLRenderer):
    def text(self, text) -> str:
        return text
    def emphasis(self, text: str) -> str:
        return '`*' + text + '`*'
    def strong(self, text: str) -> str:
        return '`!' + text + '`!'
    def codespan(self, text: str) -> str:
        return '`=' + text + '`='
    def heading(self, text, level, **attrs) -> str:
        if level > 3:
            level = 3
        return '>' * level + text + '\n'
    def link(self, text: str, url: str, title=None) -> str:
        s = self.safe_url(url)
        if text:
            s = text + '`' + s
        return f'`[{s}]'
    def image(self, text: str, url: str, title=None) -> str:
        s = self.safe_url(url)
        if title:
            s = title + '`' + s
        return f'`[{s}]'
    def blank_line(self) -> str:
        return '' + '\n'
    def linebreak(self) -> str:
        return '\n'
    def softbreak(self) -> str:
        return '\n'
    def inline_html(self, html: str) -> str:
        return '`=\n' + html + '`=\n'
    def thematic_break(self):
        return '-' + '\n'
    def paragraph(self, text):
        return text + '\n'
    def block_quote(self, text: str) -> str:
        return '>>>>' + text
    def list(self, text: str, ordered: bool, **attrs) -> str:
        return text + '\n'
    def list_item(self, text: str) -> str:
        return '+ ' + text + '\n'
    def block_code(self, code: str, info=None) -> str:
        return '`=\n' + code + '`=\n'

def main():

    parser = argparse.ArgumentParser(description="Converts a Markdown file to Micron format")
    parser.add_argument("md_file", nargs="?", default=None, help="Markdown formatted source file", type=str)
    parser.add_argument("mu_file", nargs="?", default=None, help="Micron formatted destination file", type=str)
    parser.print_usage = parser.print_help
    args = parser.parse_args()

    with open(args.md_file, 'r') as mdf:
        md_str = mdf.read()
    m2μ = Markdown2Micron()
    md2micron = mistune.create_markdown(renderer=m2μ)

    with open(args.mu_file, 'w') as muf:
        md_str = muf.write(md2micron(md_str))

if __name__ == "__main__":
	main()