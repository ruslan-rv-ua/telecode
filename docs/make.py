from pathlib import Path
import markdown

app_path = Path(__file__).parent

def make_html_docs(app_name:str, app_version:str) -> Path:
	"""Simple program that markdown to pretty Bootstrap html.

	:return: [path to generated `index.html`]
	:rtype: Path
	"""	
	""""""
	md_file = app_path / 'templates/index.md'
	md_template = md_file.read_text(encoding='utf8')
	md_text = md_template.format(app_name=app_name, app_version=app_version)
	
	html_file = app_path / 'templates/bootstrap.html'
	html_template = html_file.read_text(encoding='utf8')
	
	md = markdown.Markdown(extensions = ['meta'])
	html = md.convert(md_text)
	
	result_html = html_template.format(app_name=app_name, html=html, app_version=app_version)

	html_file = app_path / 'index.html'
	html_file.write_text(result_html, encoding='utf8')
	
	return html_file
