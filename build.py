import shutil

from py_to_win_app import Project

from docs.make import make_html_docs


class TelecodeProject(Project):
    def build(self):
        super().build(python_version="3.9.7", pydist_dir="telecode")
        print("Generating documentation.")
        make_html_docs(app_name=project.name, app_version=project.version)
        print("Done.\n")

        print("move `settings` file to app's dir")
        shutil.move(src=project.source_path / "settings", dst=project.build_path)
        print("Done\n")

if __name__ == '__main__':
    project = TelecodeProject.from_pyproject()
    project.build()
    project.make_dist(delete_build_dir=True)

    print("Finished!!!")
    print(f"The distribution zip archive is in the {project.dist_path}.")
    print("Now make release on GitHub!")
