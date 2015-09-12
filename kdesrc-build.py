#!/usr/bin/env python

"""
Usage:
    kdesrc-build.py [options] <project>...

options:
    -h --help           Show this screen.
    --version           Show version.
"""

import sys
import os
import docopt
import requests
import logging
import xml.etree.ElementTree as et

import utils.git as git
import utils.cmake as cmake
import utils.make as make

VERSION = '0.1'
SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
KDE_PROJECTS_XML_URL = 'https://projects.kde.org/kde_projects.xml'
KDEBUILD_DIR = os.path.join(os.path.expanduser('~'), 'kdebuild')
SOURCE_DIR = os.path.join(KDEBUILD_DIR, 'source')
BUILD_DIR = os.path.join(KDEBUILD_DIR, 'build')
INSTALL_DIR = os.path.join(KDEBUILD_DIR, 'install')

class BuildElement():

    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.identifier = self.xml_tree.attrib['identifier']
        self.subprojects = self._find_subprojects()
        self.deps = self._find_dependencies()

    def _find_subprojects(self):
        submodules = [BuildElement(x) for x in self.xml_tree.findall('module')]
        subprojects = [BuildElement(x) for x in self.xml_tree.findall('project')]
        return submodules + subprojects

    def _find_dependencies(self):
        return []

    def get(self):
        logging.debug('[GET] {}'.format(self.identifier))
        # create source dir
        self.source_dir = os.path.join(SOURCE_DIR, self.identifier)
        os.makedirs(self.source_dir, exist_ok=True)
        # find git url
        repo = self.xml_tree.find('repo')
        if repo:
            url_repos = [x for x in repo.findall('url')]
            for url in url_repos:
                if url.get('protocol') == 'git':
                    git.update_repo(url.text, self.source_dir)

    def build(self):
        logging.debug('[BUILD] {}'.format(self.identifier))
        # create build dir
        self.build_dir = os.path.join(BUILD_DIR, self.identifier)
        os.makedirs(self.build_dir, exist_ok=True)
        cmake.run(self.source_dir, self.build_dir, INSTALL_DIR)

    def install(self):
        logging.debug('[INSTALL] {}'.format(self.identifier))
        make.install(self.build_dir)

    def setup(self):
        [x.setup() for x in self.deps]
        [x.setup() for x in self.subprojects]
        self.get()
        self.build()
        self.install()



def find_project(xml_tree, kde_project_name):
    logging.debug('Looking for {} in kde_projects.xml'.format(kde_project_name))
    for comp in xml_tree.findall('component'):
        if comp.attrib['identifier'] == kde_project_name:
            return comp
        for mod in comp.findall('module'):
            if mod.attrib['identifier'] == kde_project_name:
                return mod
            for proj in mod.findall('project'):
                if proj.attrib['identifier'] == kde_project_name:
                    return proj
    return None

def check_kde_projects_xml(source_dir):
    file_path = os.path.join(source_dir, 'kde_projects.xml')
    if not os.path.exists(file_path):
        logging.debug('Downloading kde_projects.xml from {}'.format(KDE_PROJECTS_XML_URL))
        r = requests.get(KDE_PROJECTS_XML_URL)
        with open(file_path, 'wb') as f:
            f.write(r.content)
    return file_path

def load_kde_projects_xml():
    xml_tree = None
    xml_path = check_kde_projects_xml(SCRIPT_DIR)
    with open(xml_path, 'r') as f:
        xml_content = f.read()
        xml_tree = et.fromstring(xml_content)
    return xml_tree

def create_default_dirs():
    os.makedirs(SOURCE_DIR, exist_ok=True)
    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(INSTALL_DIR, exist_ok=True)

def init_logger():
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

def main(cmdline):
    init_logger()
    create_default_dirs()
    logging.debug(cmdline)
    xml_tree = load_kde_projects_xml()
    xml_projects = [find_project(xml_tree, x) for x in cmdline['<project>']]
    build_list = [BuildElement(x) for x in xml_projects if x is not None]
    [x.setup() for x in build_list]

if __name__ == '__main__':
    cmdline = docopt.docopt(__doc__, version=VERSION)
    excode = main(cmdline)
    sys.exit(excode)
