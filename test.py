import markdown
from bleach_whitelist import markdown_attrs, all_tags, all_styles
import bleach

value = '''The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium'''

html = bleach.linkify(bleach.clean(markdown.markdown(value, output_format='html', extensions=['extra', 'abbr']),
                                          all_tags, markdown_attrs, all_styles, strip=True))
print(html)