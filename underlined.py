__all__ = ['underlined']

import re

UNDERLINED = r'\b_{1,3}(?=[^\s_])'
UNDERLINED_END_RE = {
    '_': re.compile(r'(?:(?<!\\)(?:\\\\)*\\_|[^\s_])_(?!_)\b'),
    '__': re.compile(r'(?:(?<!\\)(?:\\\\)*\\_|[^\s_])__(?!_)\b'),
    '___': re.compile(r'(?:(?<!\\)(?:\\\\)*\\_|[^\s_])___(?!_)\b'),
}

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

def render_underlined_mu(self, token, state) -> str:
        return '`_' + self.render_children(token, state) + '`_'

def render_underlined_html(self, token, state) -> str:
        return '<u>' + self.render_children(token, state) + '</u>'

def underlined(md):
    """A mistune plugin to render underlined tags. 
    Most Markdown parsers render it as emphasis tag.

    Underlined text is surrounded by `_`, `__`, or `___`

    :param md: Markdown instance
    """
    md.inline.register('underlined', UNDERLINED, parse_underlined, before='emphasis')
    if md.renderer: 
        if md.renderer.NAME == 'html':
            md.renderer.register('underlined', render_underlined_html)
        elif md.renderer.NAME == 'micron':
            md.renderer.register('underlined', render_underlined_mu)
