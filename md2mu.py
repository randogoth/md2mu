import mistune
from mistune import Markdown
from mistune.core import BlockState
from mistune.util import strip_end
from mistune.renderers._list import render_list
from mistune.renderers.markdown import MarkdownRenderer
from typing import Dict, Any
from textwrap import indent
import argparse
import re

UNDERLINED = r'\b_{1,3}(?=[^\s_])'
UNDERLINED_END_RE = {
    '_': re.compile(r'(?:(?<!\\)(?:\\\\)*\\_|[^\s_])_(?!_)\b'),
    '__': re.compile(r'(?:(?<!\\)(?:\\\\)*\\_|[^\s_])__(?!_)\b'),
    '___': re.compile(r'(?:(?<!\\)(?:\\\\)*\\_|[^\s_])___(?!_)\b'),
}

def parse_underlined(inline, m, state):
    text = m.group(2)
    print('rrr')
    state.append_token({'type': 'underlined', 'raw': text})
    return m.end()

def parse_underlined(self, m, state) -> int:
        pos = m.end()
        marker = m.group(0)
        mlen = len(marker)
        _end_re = UNDERLINED_END_RE[marker]
        m1 = _end_re.search(state.src, pos)
        if not m1:
            state.append_token({'type': 'text', 'raw': marker})
            return pos
        end_pos = m1.end()
        text = state.src[pos:end_pos-mlen]
        prec_pos = self.precedence_scan(m, state, end_pos)
        if prec_pos:
            return prec_pos
        new_state = state.copy()
        new_state.src = text
        new_state.in_underlined = True
        state.append_token({
            'type': 'underlined',
            'children': self.render(new_state),
        })
        return end_pos

def render_underlined(self, token, state) -> str:
        return '`_' + self.render_children(token, state) + '`_'

class Markdown2Micron(MarkdownRenderer):
    NAME = 'micron'

    def __call__(self, tokens, state: BlockState):
        out = self.render_tokens(tokens, state)
        # special handle for line breaks
        out += '\n\n'.join(self.render_referrences(state)) + '\n'
        return strip_end(out)
    
    def render_children(self, token, state: BlockState):
        children = token['children']
        return self.render_tokens(children, state)

    def text(self, token: Dict[str, Any], state: BlockState) -> str:
        return token['raw']
    
    def emphasis(self, token: Dict[str, Any], state: BlockState) -> str:
        return '`*' + self.render_children(token, state) + '`*'

    def strong(self, token: Dict[str, Any], state: BlockState) -> str:
        return '`!' + self.render_children(token, state) + '`!'
    
    def link(self, token: Dict[str, Any], state: BlockState) -> str:
        label = token.get('label')
        text = self.render_children(token, state)
        out = '`[' + text + '`'
        if label:
            return out + '`[' + label + '`'
        attrs = token['attrs']
        url = attrs['url']
        if text == url:
            return '`[' + text + '`'
        elif 'mailto:' + text == url:
            return '`[' + text + '`'
        out += url
        return out + ']'
    
    def image(self, token: Dict[str, Any], state: BlockState) -> str:
        return self.link(token, state)

    def codespan(self, token: Dict[str, Any], state: BlockState) -> str:
        return '`=' + token['raw'] + '`='

    def linebreak(self, token: Dict[str, Any], state: BlockState) -> str:
        return '  \n'
    
    def softbreak(self, token: Dict[str, Any], state: BlockState) -> str:
        return '\n'
    
    def blank_line(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''
    
    def inline_html(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''
    
    def paragraph(self, token: Dict[str, Any], state: BlockState) -> str:
        text = self.render_children(token, state)
        return text + '\n\n'

    def heading(self, token: Dict[str, Any], state: BlockState) -> str:
        level = token['attrs']['level']
        if level > 3:
            level = 3
        marker = '>' * level
        text = self.render_children(token, state)
        return marker + ' ' + text + '\n\n'
    def thematic_break(self, token: Dict[str, Any], state: BlockState) -> str:
        return '-\n\n'
    
    def block_text(self, token: Dict[str, Any], state: BlockState) -> str:
        return self.render_children(token, state) + '\n'
    
    def block_code(self, token: Dict[str, Any], state: BlockState) -> str:
        code = token['raw']
        if code and code[-1] != '\n':
            code += '\n'
        marker = '`='
        return marker + '\n' + code + marker + '\n\n'
    
    def block_quote(self, token: Dict[str, Any], state: BlockState) -> str:
        text = indent(self.render_children(token, state), '>>>>')
        return text + '\n\n'
    
    def block_html(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''
    
    def block_error(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''
    
    def list(self, token: Dict[str, Any], state: BlockState) -> str:
        return render_list(self, token, state)

def m2μ():
    m2μr = Markdown2Micron()
    m2μ = Markdown(renderer=m2μr)
    m2μ.inline.register('underlined', UNDERLINED, parse_underlined, before='emphasis')
    m2μ.renderer.register('underlined', render_underlined)
    return m2μ

def main():

    parser = argparse.ArgumentParser(description="Converts a Markdown file to Micron format")
    parser.add_argument("md_file", nargs="?", default=None, help="Markdown formatted source file", type=str)
    parser.add_argument("mu_file", nargs="?", default=None, help="Micron formatted destination file", type=str)
    parser.print_usage = parser.print_help
    args = parser.parse_args()

    with open(args.md_file, 'r') as mdf:
        md_str = mdf.read()
    md2mu = m2μ()

    with open(args.mu_file, 'w') as muf:
        md_str = muf.write(md2mu(md_str))

if __name__ == "__main__":
	main()