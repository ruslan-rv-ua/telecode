from pathlib import Path
import markdown

INPUT = 'index.md'

def make():
	"""Simple program that markdown to pretty Bootstrap html."""
	file = Path(__file__).parent / INPUT
	md_text = file.read_text(encoding='utf8')
	
	template_file = Path(__file__).parent / 'templates/bootstrap.html'
	template = template_file.read_text(encoding='utf8')
	
	md = markdown.Markdown(extensions = ['meta'])
	html = md.convert(md_text)
	
	application = md.Meta['application'][0]
	version = md.Meta['version'][0]
	
	result_html = template.format(application=application, html=html, version=version)
	
	file.with_suffix('.html').write_text(result_html, encoding='utf8')
	

if __name__ == '__main__':
	make()