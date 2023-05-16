from mistune.core import BlockState
from mistune.util import strip_end
from mistune.renderers._list import render_list
from mistune.renderers.markdown import MarkdownRenderer
from typing import Dict, Any
from textwrap import indent

class MicronRenderer(MarkdownRenderer):
    """A renderer to format Micron text."""
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