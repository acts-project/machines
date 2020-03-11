#!/usr/bin/env python

# Author: Ivan Razumov
# Usage: lcgview.py [options] <view_root>
# This package creates a "view" of LCG release in folder <view_root>.
# optional arguments:
#    -h, --help                       show this help message and exit
#    -l LCGPATH, --lcgpath LCGPATH    top directory of LCG releases (default: /afs/cern.ch/sw/lcg/releases)
#    -r LCGREL, --release LCGREL      LCG release number (default: 80)
#    -p LCGPLAT, --platform LCGPLAT   Platform to use (default: x86_64-slc6-gcc49-opt)
#    -d, --delete                     delete old view before creating a new one
#    -s, --package-selection          Create view only from packages specified in file. For experts only.
#    -B, --enable-blacklists          Enable built-in blacklists of files and packages. For experts only.
#    -D, --dry-run                    Don't make changes to the file system
#    -v, --verbose                    Increase logging verbosity
#    -q, --quiet                      Decrease logging verbosity
#    --loglevel LEVEL                 Change logging level
#    --version                        show program's version number and exit

import argparse
import glob
import logging
import os
import re
import shutil
import sys
import time
from collections import defaultdict, OrderedDict


class LCGViewMaker(object):
    def __init__(self, lcgpath, lcgrel, lcgplat, pkgfile, view_destination, blacklist, greylist, pkg_blacklist,
                 dry_run, prioritylist):
        super(LCGViewMaker, self).__init__()
        self.lcg_root = lcgpath
        self.lcg_release = lcgrel
        self.lcg_platform = lcgplat
        self.lcg_naked_platform = self.get_naked_platform(lcgplat)
        self.lcg_packages = []
        self.view_root = view_destination
        self.externals = defaultdict(OrderedDict)
        self.blacklist = blacklist
        self.greylist = greylist
        self.pkg_blacklist = pkg_blacklist
        self.topdir_whitelist = ['aclocal', 'cmake', 'emacs', 'fonts', 'include', 'macros', 'test', 'tests', 'plugins',
                                 'bin', 'config', 'etc', 'icons', 'lib', 'lib64', 'libexec', 'man', 'tutorials', 'share', 'src', 'jre', 'mkspecs',
                                 'scripts', 'python', 'nvvm']
        self.concatenatelist = ['easy-install.pth']
        self.dry_run = dry_run
        self.prioritylist = prioritylist

        self.packages_to_install = {}
        self.compiler = None

        if pkgfile:
            with open(pkgfile, "r") as pkgfd:
                for line in pkgfd.readlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    data = [x.strip() for x in line.split(" ")]
                    if len(data) == 1:
                        data.append("")

                    self.lcg_packages.append(data)

    def get_default_version(self, package):
        if package not in self.externals:
            logging.error("Package %s not known when choosing default version!", package)
            return None

        all_versions = self.externals[package].keys()
        return sorted(all_versions)[-1]

    def add_externals_from_release_file(self, lcg_file):
        txt_file = open(lcg_file)
        for line in txt_file.readlines():
            if line.startswith('COMPILER:'):
                self.compiler = [x.strip() for x in line[10:].split(';')]
                continue
            try:
                name, pkghash, version, home, deps = [x.strip() for x in line.split(';')]
            except ValueError:
                continue
            else:
                r = {'NAME': name, 'HASH': pkghash, 'HOME': home,
                     'VERSION': version, 'DEPS': [x.split('-') for x in deps.split(',')]}
                self.externals[name][version] = r

    def splitall(self, path):
        allparts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path:  # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])
        return allparts

    def add_externals_from_directory(self, directory, platform):
        dirs = glob.glob(os.path.join(directory, '*/*', platform))
        dirs.extend(glob.glob(os.path.join(directory, '*/*/*', platform)))
        naked_platform = self.get_naked_platform(platform)
        if(naked_platform != platform) :
            dirs.extend(glob.glob(os.path.join(directory, '*/*', naked_platform)))
            dirs.extend(glob.glob(os.path.join(directory, '*/*/*', naked_platform)))
        for d in dirs:
            p = self.splitall(d)
            name = p[-3]
            version = p[-2]
            deps = []
            hash = ''
            # do not add the same package with same version for the naked platform
            if name in self.externals and version in self.externals[name] : continue
            try :
              data = {}
              line = open(os.path.join(d,'.buildinfo_%s.txt'%name)).readlines()[0]
              line = line.replace('"format:','"')  # support old installations
              text = line.split(', ')
              for key, value in [x.split(':') for x in text]:
                data.update({key.strip(): value.strip()})
              deps = [x.split('-')[::2] for x in data['DEPENDS'].split(',') if len(x) != 0]
              hash = data['HASH']
            except:
              pass
            r = {'NAME': name, 'VERSION': version, 'HOME': d.replace(directory, '.'), 'DEPS': deps, 'HASH':hash}
            self.externals[name][version] = r

    def get_naked_platform(self, orig):
        arch, osvers, compvers, buildtype = orig.split('-')
        return '-'.join([arch.split('+')[0], osvers, compvers, buildtype])

    def write_setup(self):
        if self.dry_run:
            return
        arch, osvers = self.lcg_naked_platform.split('-')[:2]
        compiler_found = False

        if self.compiler:
            compiler, version = self.compiler
            logging.debug('Setting compiler from self.compiler: {0}, {1}'.format(compiler, version))
        else: 
            arch, osvers, compvers, buildtype = self.lcg_naked_platform.split('-')
            if 'COMPILER' in os.environ and os.environ['COMPILER'].lower() != 'native' : 
                compvers = os.environ['COMPILER']
            patt = re.compile('([a-z]+)([0-9]+)([a-z]*)')
            mobj = patt.match(compvers)
            compiler = mobj.group(1)
            version = '.'.join(list(mobj.group(2))) + mobj.group(3)
            logging.debug('Setting compiler from environment: {0}, {1}'.format(compiler, version))
        for p in (os.path.join(i,j) for i in ('.', '..', '../../../..', '../../..', '../..') for j in ('contrib','external','.')):
            logging.debug('Looking for compiler ({0}, {1}) in {2}'.format(compiler, version, p))
            logging.debug('... aka ' + os.path.join(self.lcg_root, p, compiler, version))
            logging.debug('... norm ' + os.path.normpath(os.path.join(self.lcg_root, p, compiler, version)))
            if os.path.exists(os.path.normpath(os.path.join(self.lcg_root, p, compiler, version))):
                compiler = os.path.normpath(os.path.join(self.lcg_root, p, compiler, version, '-'.join((arch, osvers))))
                logging.debug('Compiler found in ' + compiler)
                compiler_found = True
                break

        if not compiler_found:
            logging.warn("Compiler '{0}' version '{1}' for OS '{2}' and architecture '{3}' not found!".format(compiler, version, osvers, arch))

        thisdir = os.path.dirname(os.path.realpath(__file__))
        setup_sh  = open(os.path.join(thisdir,'create_lcg_view_setup_sh.in')).read()
        setup_csh = open(os.path.join(thisdir,'create_lcg_view_setup_csh.in')).read()
        f = open(os.path.join(self.view_root, 'setup.sh'), 'w')
        f.write(setup_sh.replace('@date@', time.strftime("%c"))
                        .replace('@compilerlocation@', compiler)
                        .replace('@lcg_version@',os.getenv('LCG_VERSION','')))
        f.close()
        f = open(os.path.join(self.view_root, 'setup.csh'), 'w')
        f.write(setup_csh.replace('@date@', time.strftime("%c"))
                         .replace('@compilerlocation@', compiler)
                         .replace('@lcg_version@',os.getenv('LCG_VERSION','')))
        f.close()

    def getPackageName(self, directory):
        name = directory.split("/")[0]
        if name == "MCGenerators" or name == "Grid":
            name = directory.split("/")[1]
        return name

    def install_pkg(self, pkg_name, pkg_version):
        logging.debug('Installing {0} version {1}'.format(pkg_name, pkg_version))
        if self.dry_run:
            return

        if self.lcg_release :
            if not self.lcg_release.startswith('LCG_') :
                release_root = os.path.join(self.lcg_root, 'LCG_%s' % self.lcg_release)
            else :
                release_root = os.path.join(self.lcg_root, self.lcg_release)
        else :
            release_root = self.lcg_root

        pkg_root = os.path.realpath(os.path.join(release_root, self.externals[pkg_name][pkg_version]['HOME']))
        logging.info('Package {0} ver. {1}: root = {2}'.format(pkg_name, pkg_version, pkg_root))

        for (dir_path, dirnames, filenames) in os.walk(pkg_root, followlinks=False):
            if 'doc' in self.splitall(dir_path):
                continue

            if 'logs' in self.splitall(dir_path):
                continue

            dirpath = dir_path.replace(pkg_root, '.')
            dirpath_s = self.splitall(dirpath)

            # Elinimate any top level file or directory not in the topdir_whitelist
            if len(dirpath_s) == 1 or dirpath_s[1] not in self.topdir_whitelist:
                continue


            view_dir = os.path.realpath(os.path.join(self.view_root, dirpath))
 
            if not os.path.exists(view_dir):
                # print 'Create directory', os.path.realpath(os.path.join(view_root, dirpath))
                try:
                    os.makedirs(view_dir)
                except OSError as e:
                    if e.errno == 20:
                        logging.warning("Target already exisits and is file: {0}".format(view_dir))
                        logging.info("Added from: {0}".format(os.path.realpath(view_dir)))
                        logging.info("Conflicts with: {0}".format(os.path.realpath(dir_path)))
                    else:
                        raise e

            for d in dirnames:
                source = os.path.join(dir_path, d)
                target = os.path.join(view_dir, d)
                if os.path.islink(source) and not os.path.exists(target):
                    os.symlink(os.readlink(source), target)

            for f in filenames:
                if f in self.blacklist or f.startswith('.') or f.endswith('-env.sh') or f.endswith('~'):
                    continue

                source = os.path.join(dir_path, f)
                target = os.path.join(view_dir, f)

                source_rel = os.path.realpath(source).replace(self.lcg_root + os.path.sep, '')
                target_rel = os.path.realpath(target).replace(self.lcg_root + os.path.sep, '')

                if f in self.concatenatelist:
                    open(target, 'a').write(open(source, 'r').read())
                    continue

                if not os.path.exists(target):
                    # print "Create symlink: {0} -> {1}".format(source, target)
                    try:
                        os.symlink(source, target)
                    except OSError as e:
                        if e.errno == 20:
                            logging.warning("Target already exisits and is file: {0}".format(f))
                            logging.info("Added from: {0}".format(os.path.realpath(target_rel)))
                            logging.info("Conflicts with: {0}".format(os.path.realpath(source_rel)))
                        else:
                            raise e
                else:
                    if f not in self.greylist:
                        logging.warning("File already exists: {0}".format(target))
                        logging.info("Added from: {0}".format(target_rel))
                        logging.info("Conflicts with: {0}".format(source_rel))
                        # return 1
                        # Check priority list
                        if pkg_name in self.prioritylist:
                            # Remove previous installed one and force to install the priority pkg_name
                            os.remove(target)
                            os.symlink(source, target)
                            logging.info("Package with priority: {0}".format(pkg_name))
                            logging.info("Replacing file, now added by: {0}".format(source_rel))
                        else:
                            logging.info("Package with priority: {0}".format(self.getPackageName(target_rel)))
                            logging.info("File keeps added from: {0}".format(target_rel))


    def prepare_package(self, pkgname, pkgversion):
        if pkgname in self.packages_to_install:
            logging.debug("Package {0} already added".format(pkgname))
            return

        if pkgname in self.externals:
            if pkgversion in self.externals[pkgname] or pkgversion == '':
                if pkgversion == '':
                    pkgversion = self.get_default_version(pkgname)
                    logging.info(
                        "Package version for {0} not specified, substituting {1}".format(pkgname, pkgversion))

                self.packages_to_install[pkgname] = pkgversion
                logging.debug("Add package {0} version {1}".format(pkgname, pkgversion))
                if not self.lcg_packages : return # no need to look at dependencies
                logging.debug(
                    "Add {0} dependencies: {1}".format(len(self.externals[pkgname][pkgversion]['DEPS']),
                                                       self.externals[pkgname][pkgversion]['DEPS']))
                for dep in self.externals[pkgname][pkgversion]['DEPS']:
                    if len(dep) != 2:
                        continue

                    depname, dephash = dep
                    depver = ''
                    for depv, depd in self.externals[depname].iteritems():
                        if depd['HASH'] == dephash:
                            depver = depv
                            break

                    if depver != '':
                        logging.debug("Add dependency: {0} version {1}".format(depname, depver))
                        if depname in self.packages_to_install and self.packages_to_install[depname] != depver :
                            logging.info(
                                "Dependency override: package {0}, version {1} -> {2}".format(depname, pkg[1], depver))
                            self.packages_to_install[depname] = depver
                        # recursive call to prepare_package
                        self.prepare_package(depname, depver)
                    else:
                        logging.critical(
                            "Package {0} with hash {1} not found in release {2} when processing package "
                            "{3} version {4}".format(depname, dephash, self.lcg_release, pkgname, pkgversion))
                        return 1
            else:
                logging.critical(
                    "Version {1} of package {0} not found in release {2}!".format(pkgname, pkgversion,
                                                                                  self.lcg_release))
                logging.info("Possible versions: {0}".format(", ".join(self.externals[pkgname].keys())))
                return 1
        else:
            logging.critical("Package {0} not found in release {1}!".format(pkgname, self.lcg_release))
            return 1

        pass

    def make_view(self):
        # ---Check whether the LCG release actually exists, otherwise take all the packages in the root directory
        logging.debug("make_view start")
        release_root = os.path.join(self.lcg_root, 'LCG_%s' % self.lcg_release)
        if os.path.exists(release_root):
            lcg_file = os.path.join(release_root, 'LCG_externals_%s.txt' % self.lcg_platform)
            mc_file = os.path.join(release_root, 'LCG_generators_%s.txt' % self.lcg_platform)
            self.add_externals_from_release_file(lcg_file)
            self.add_externals_from_release_file(mc_file)
        else:
            release_root = self.lcg_root
            self.add_externals_from_directory(release_root, self.lcg_platform)
            self.lcg_release = None

        logging.debug("Loaded {0} externals".format(len(self.externals)))
        self.packages_to_install = {}

        if self.lcg_packages:
            logging.debug("Build view from {0} packages".format(len(self.lcg_packages)))
            for pkgname, pkgversion in self.lcg_packages:
                self.prepare_package(pkgname, pkgversion)
        else:
            logging.debug("No package list specified")
            for pkgname in self.externals:
                self.prepare_package(pkgname, max(self.externals[pkgname]))

        logging.debug("Final list contains {0} packages".format(len(self.packages_to_install)))
        for pkgname in self.pkg_blacklist:
            if pkgname in self.packages_to_install:
                self.packages_to_install.pop(pkgname)

        logging.debug("Filtered list contains {0} packages".format(len(self.packages_to_install)))

        for pkgname, pkgversion in self.packages_to_install.iteritems():
            self.install_pkg(pkgname, pkgversion)

        # ---Finalize the view with additional operations------------------------------------------------------------
        self.write_setup()


def main():
    helpstring = """{0} [options] <view_destination>

This package creates a "view" of LCG release in folder <view_destination>.
"""

    # lcg_root = '/afs/cern.ch/sw/lcg/releases'
    # lcg_release = 79
    # lcg_platform = 'x86_64-slc6-gcc49-opt'
    # view_root = '/tmp/view_{0}{1}'.format(lcg_release, lcg_platform)

    parser = argparse.ArgumentParser(usage=helpstring.format(sys.argv[0]))
    parser.add_argument('view_destination', metavar='view_destination', nargs='+', help=argparse.SUPPRESS)
    parser.add_argument('-l', '--lcgpath', help="top directory of LCG releases (default: /afs/cern.ch/sw/lcg/releases)",
                        action="store",
                        default='/afs/cern.ch/sw/lcg/releases', dest='lcgpath')
    parser.add_argument('-r', '--release', help="LCG release number (default: 80)", action="store", default=80,
                        dest="lcgrel")
    parser.add_argument('-p', '--platform', help="Platform to use (default: x86_64-slc6-gcc49-opt)", action="store",
                        default='x86_64-slc6-gcc49-opt', dest='lcgplat')
    parser.add_argument('-d', '--delete', help="delete old view before creating a new one", action="store_true",
                        default=False, dest='delview')
    parser.add_argument('-B', '--enable-blacklists',
                        help='Enable built-in blacklists of files and packages. For experts only.',
                        action="store_true", dest='bl_enabled')
    parser.add_argument('-s', '--package-selection',
                        help='Create view only from packages specified in file. For experts only.',
                        action='store', dest='pkgfile')
    parser.add_argument('-D', '--dry-run',
                        help="Don't delete or link anything. For debugging only.", action='store_true', dest='dry_run')
    parser.add_argument('-c', '--conflict', help="List of packages with priority in conflicts", default=[],nargs='+', type=str, dest='prioritylist')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='count', dest='verbose_level', help='Increase logging verbosity',
                       default=0)
    group.add_argument('-q', '--quiet', action='count', dest='quiet_level', help='Decrease logging verbosity',
                       default=0)
    group.add_argument('--loglevel', choices=['ERROR', 'WARNING', 'INFO', 'DEBUG'], action='store',
                       dest='loglvl', default='INFO', help='Set logging level (default: INFO)')
    args = parser.parse_args()
    parser.add_argument('--version', action='version', version='%(prog)s 0.5')

    loglvl = min(logging.ERROR,
                 max(logging.DEBUG,
                     getattr(logging, args.loglvl.upper()) - args.verbose_level * 10 + args.quiet_level * 10))

    logging.basicConfig(format=u'*** %(levelname)s: %(message)s', level=loglvl)
    # print "Logging config: {0} + {1} - {2} = {3}".format(args.loglvl.upper(), args.verbose_level * 10,
    #                                                      args.quiet_level * 10, logging.getLevelName(loglvl))

    if args.bl_enabled:
        blacklist = ['.filelist', 'README',
                     'LICENSE', 'decimal.h', 'project.cmt', 'INSTALL', 'dir']
        greylist = ['site.py', 'site.pyc', 'easy_install', 'easy_install-2.7', 'setuptools.pth',
                    'pytest', 'f2py', 'fcc']
        pkg_blacklist = ['neurobayes_expert', 'cmt', 'xrootd_python', 'hepmc3',  
                         'powheg-box', 'sherpa-mpich2',
                         'pyanalysis', 'pytools', 'pygraphics', 'PythonFWK']
    else:
        blacklist = ['version.txt']
        greylist = []
        pkg_blacklist = []

    # hack until hepmc3 is fixed!
    if re.compile('.*(geantv|hsf)').match(os.getenv('LCG_VERSION','')):
        pkg_blacklist.remove('hepmc3')
        pkg_blacklist.append('HepMC')

    if args.delview and os.path.exists(args.view_destination[0]):
        shutil.rmtree(args.view_destination[0], True)

    if not os.path.exists(args.view_destination[0]):
        os.makedirs(args.view_destination[0])

    if args.pkgfile and not os.path.exists(args.pkgfile):
        logging.critical("Package selection file {0} does not exist!".format(args.pkgfile))
        return 1

    v = LCGViewMaker(lcgpath=args.lcgpath, lcgrel=args.lcgrel, lcgplat=args.lcgplat, pkgfile=args.pkgfile,
                     view_destination=args.view_destination[0], blacklist=blacklist, greylist=greylist,
                     pkg_blacklist=pkg_blacklist, dry_run=args.dry_run, prioritylist=args.prioritylist)

    return v.make_view()

    # return 0

if __name__ == '__main__':
    exit(main())
