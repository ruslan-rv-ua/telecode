import shutil

from toml import load

import py2winapp
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

# generate docs
html_doc_file_path = make_html_docs(app_name=APP_NAME, app_version=APP_VERSION)

# move `settings` file to app's dir
shutil.move(src=build.source_subdir_path / 'settings', dst=build.app_dir_path)

# remove all `*.zip` in `docs` folder
for file in (build.project_dir_path / 'docs').rglob('*.zip'):
	file.unlink()
# make zip distribution in `docs` folder
build.make_zip(file_name=APP_FOLDER, destination_dir=build.project_dir_path / 'docs')

# ...and delete app folder!
shutil.rmtree(build.app_dir_path)

