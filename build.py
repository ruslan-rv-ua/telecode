import py2winapp
import shutil
from toml import load

from docs.make import make_html_docs

project_data = load('pyproject.toml')
APP_NAME = project_data['tool']['poetry']['name']
APP_VERSION = project_data['tool']['poetry']['version']
APP_FOLDER = f'{APP_NAME}-{APP_VERSION}'


build = py2winapp.build(
    python_version="3.9.7",
	input_dir=f'{APP_NAME}',
	main_file_name="main.py",
	app_dir=APP_FOLDER,
	source_subdir=APP_NAME,
	show_console=False,
)

build.rename_exe_file(APP_NAME)

# make zip in `docs` folder
build.make_zip(file_name=APP_FOLDER, destination_dir=build.project_dir_path / 'docs')

# generate docs, copy to app's folder
html_doc_file_path = make_html_docs(app_name=APP_NAME, app_version=APP_VERSION)
shutil.copyfile(src=html_doc_file_path, dst=build.source_subdir_path / 'docs.html')