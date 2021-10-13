import py2winapp

APP_NAME = 'telecode'

build = py2winapp.build(
    python_version="3.9.7",
	input_dir=f'{APP_NAME}',
	main_file_name="main.py",
	app_dir=APP_NAME,
	source_subdir=APP_NAME,
	# show_console=True,
)

build.rename_exe_file(APP_NAME)
# build.make_zip(APP_NAME)