"""Get implementations for middlewares."""

from git import Repo, Git
from os import makedirs, path
from shutil import rmtree
from ..definitions import PIDEVICES_IMPLS, IMPLS_PATH


class ImplementationsGetter():

    repos = {"pidevices": "https://github.com/robotics-4-all/tektrain-robot-sw"}

    def __init__(self, middleware):
        """Contructor"""

        self.middleware = middleware
        self.repo = self.repos[middleware]
        filepath = path.abspath(path.dirname(__file__)) + "/"
        self.tmp_dir = filepath + "tmp"

    def get_repo(self, branch=None):
        """Get a repo from github"""
        # Create tmp directory
        if not path.exists(self.tmp_dir):
            makedirs(self.tmp_dir)

        Repo.clone_from(self.repo, self.tmp_dir)
        git = Git(self.tmp_dir)
        if branch:
            git.checkout(branch)

    def remove_repo(self):
        if path.exists(self.tmp_dir):
            # Delete tmp directory
            rmtree(self.tmp_dir)

    def get(self):
        if self.middleware == "pidevices":
            func = self.get_pidevices

        return func()

    def get_pidevices(self):
        # Create if it doesn't exist the txt file
        if not path.exists(PIDEVICES_IMPLS):
            self.update_pidevices("better_imports")

        return self.read_conf(PIDEVICES_IMPLS)

    def read_conf(self, conf_path):
        with open(conf_path, "r") as f:
            lines = f.readlines()

        impls = []
        for line in lines[2:]:
            impls.append(line.strip("\n"))

        return impls

    def update_pidevices(self, branch=None):
        # Create implementations folder
        if not path.exists(IMPLS_PATH):
            makedirs(IMPLS_PATH)

        self.get_repo(branch)

        impls = self.get_names("/pidevices/sensors/__init__.py")
        impls += self.get_names("/pidevices/actuators/__init__.py")

        # Save to config for m2t
        lines = ["# Implementations for pidevices middleware. \n"]
        self.save(PIDEVICES_IMPLS, impls, lines)

        self.remove_repo()

    def save(self, f_path, names, lines):
        # Read lines
        if path.exists(PIDEVICES_IMPLS):
            with open(f_path, "r") as f:
                lines = f.readlines()

        # Change namespace
        new_lines = []
        new_lines.append(lines[0])
        new_lines.append("\n")
        for name in names:
            new_lines.append(name + "\n")

        # Write back
        with open(f_path, "w") as f:
            f.writelines(new_lines)

    def get_names(self, f_path):
        with open(self.tmp_dir + f_path, "r") as f:
            lines = f.readlines()

        names = []
        for line in lines:
            splitted = line.strip("\n").split("import")
            if len(splitted) > 1:
                possible = splitted[-1].strip(" ")
                if possible != "*":
                    for clss in possible.split(","):
                        names.append(clss.strip(" "))
        return names
