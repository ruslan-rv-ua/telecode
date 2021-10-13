from pathlib import Path
import markdown

INPUT_FILE = 'index.md'

app_path = Path(__file__).parent

def make_html_docs() -> Path:
	"""Simple program that markdown to pretty Bootstrap html.

	:return: [path to generated `index.html`]
	:rtype: Path
	"""	
	""""""
	md_file = app_path / INPUT_FILE
	md_text = md_file.read_text(encoding='utf8')
	
	template_file = app_path / 'templates/bootstrap.html'
	template = template_file.read_text(encoding='utf8')
	
	md = markdown.Markdown(extensions = ['meta'])
	html = md.convert(md_text)
	
	application = md.Meta['application'][0]
	version = md.Meta['version'][0]
	
	result_html = template.format(application=application, html=html, version=version)

	html_file = md_file.with_suffix('.html')
	html_file.write_text(result_html, encoding='utf8')
	
	return html_file	

if __name__ == '__main__':
	make_html_docs()