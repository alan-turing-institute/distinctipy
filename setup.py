import sys
from os.path import exists

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_version(fpath):
    """
    Statically parse the version number from a python file
    """
    import ast

    if not exists(fpath):
        raise ValueError("fpath={!r} does not exist".format(fpath))
    with open(fpath, "r") as file_:
        sourcecode = file_.read()
    pt = ast.parse(sourcecode)

    class Finished(Exception):
        pass

    class VersionVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                if getattr(target, "id", None) == "__version__":
                    self.version = node.value.s
                    raise Finished

    visitor = VersionVisitor()
    try:
        visitor.visit(pt)
    except Finished:
        pass
    return visitor.version


def parse_requirements(fname="requirements.txt", with_version=False):
    """
    Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    Args:
        fname (str): path to requirements file
        with_version (bool, default=False): if true include version specs

    Returns:
        List[str]: list of requirements items
    """
    import re
    from os.path import dirname, exists, join

    require_fpath = fname

    def parse_line(line, dpath=""):
        """
        Parse information from a line in a requirements text file

        line = 'git+https://a.com/somedep@sometag#egg=SomeDep'
        line = '-e git+https://a.com/somedep@sometag#egg=SomeDep'
        """
        # Remove inline comments
        comment_pos = line.find(" #")
        if comment_pos > -1:
            line = line[:comment_pos]

        if line.startswith("-r "):
            # Allow specifying requirements in other files
            target = join(dpath, line.split(" ")[1])
            for info in parse_require_file(target):
                yield info
        else:
            # See: https://www.python.org/dev/peps/pep-0508/
            info = {"line": line}
            if line.startswith("-e "):
                info["package"] = line.split("#egg=")[1]
            else:
                if ";" in line:
                    pkgpart, platpart = line.split(";")
                    # Handle platform specific dependencies
                    # setuptools.readthedocs.io/en/latest/setuptools.html
                    # #declaring-platform-specific-dependencies
                    plat_deps = platpart.strip()
                    info["platform_deps"] = plat_deps
                else:
                    pkgpart = line
                    platpart = None

                # Remove versioning from the package
                pat = "(" + "|".join([">=", "==", ">"]) + ")"
                parts = re.split(pat, pkgpart, maxsplit=1)
                parts = [p.strip() for p in parts]

                info["package"] = parts[0]
                if len(parts) > 1:
                    op, rest = parts[1:]
                    version = rest  # NOQA
                    info["version"] = (op, version)
            yield info

    def parse_require_file(fpath):
        dpath = dirname(fpath)
        with open(fpath, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    for info in parse_line(line, dpath=dpath):
                        yield info

    def gen_packages_items():
        if exists(require_fpath):
            for info in parse_require_file(require_fpath):
                parts = [info["package"]]
                if with_version and "version" in info:
                    parts.extend(info["version"])
                if not sys.version.startswith("3.4"):
                    # apparently package_deps are broken in 3.4
                    plat_deps = info.get("platform_deps")
                    if plat_deps is not None:
                        parts.append(";" + plat_deps)
                item = "".join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages


VERSION = parse_version("distinctipy/__init__.py")

setuptools.setup(
    name="distinctipy",
    version=VERSION,
    author="Jack Roberts",
    author_email="jroberts@turing.ac.uk",
    description="A lightweight package for generating visually distinct colours.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alan-turing-institute/distinctipy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
        "Framework :: Matplotlib",
    ],
    keywords="color colour palette colormap colorblind colourblind",
    packages=setuptools.find_packages(),
    install_requires=parse_requirements("requirements/runtime.txt"),
    extras_require={
        "all": parse_requirements("requirements.txt"),
        "tests": parse_requirements("requirements/tests.txt"),
        "docs": parse_requirements("requirements/docs.txt"),
        "optional": parse_requirements("requirements/optional.txt"),
    },
)
