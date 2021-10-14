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

print("move `settings` file to app's dir")
shutil.move(src=build.source_subdir_path / 'settings', dst=build.app_dir_path)
print('Done\n')

# prepare release distribution
dist_dir_path = build.project_dir_path / 'dist'
dist_files = f'{APP_NAME}*.zip'
print(f'remove all `{dist_files}` in `dist` folder')
for file in dist_dir_path.rglob(dist_files):
	file.unlink()
print('Done\n')
print('make zip distribution in `dist` folder')
build.make_zip(file_name=APP_FOLDER, destination_dir=dist_dir_path)
print('Done\n')

print('and delete app folder!')
shutil.rmtree(build.app_dir_path)
print('Done\n')

print('Finished!!!')
print(f'The distribution zip archive is in the {dist_dir_path}.')
print('Now make release on GitHub!')
