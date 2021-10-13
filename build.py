import py2winapp
import shutil

from docs.make import make_html_docs

APP_NAME = 'telecode'

build = py2winapp.build(
    python_version="3.9.7",
	input_dir=f'{APP_NAME}',
	main_file_name="main.py",
	source_subdir=APP_NAME,
	show_console=True,
)

build.rename_exe_file(APP_NAME)

# make zip in `docs` folder
build.make_zip(file_name=APP_NAME, destination_dir=build.project_dir_path / 'docs')

# generate docs, copy to app's folder
html_doc_file_path = make_html_docs()
shutil.copyfile(src=html_doc_file_path, dst=build.source_subdir_path / 'docs.html')