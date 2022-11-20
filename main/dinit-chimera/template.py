pkgname = "dinit-chimera"
_commit = "307b91e966fc9bb16b6240a1f3805b0c996ab530"
pkgver = "0.1"
pkgrel = 0
build_style = "makefile"
makedepends = ["linux-headers"]
depends = ["dinit", "util-linux", "eudev"]
pkgdesc = "Chimera core services suite"
maintainer = "q66 <q66@chimera-linux.org>"
license = "BSD-2-Clause"
url = f"https://github.com/chimera-linux/dinit-chimera"
source = f"https://github.com/chimera-linux/dinit-chimera/archive/{_commit}.tar.gz"
sha256 = "570063019a8a54bf638acd51cf24579e5734ff4c7b659eb9143e55935bbee765"
# no tests
options = ["!check", "brokenlinks"]

def post_install(self):
    self.install_file(self.files_path / "hostname", "etc")
    self.install_file(self.files_path / "locale.conf", "etc")
    # init symlink
    self.install_link("dinit", "usr/bin/init")
    # x11 support
    self.install_dir("etc/X11/Xsession.d")
    self.install_file(
        self.files_path / "01dinit-env", "etc/X11/Xsession.d", mode = 0o755
    )

@subpackage("dinit-chimera-x11")
def _x11(self):
    self.pkgdesc = f"{pkgdesc} (X11 support)"
    self.depends = [f"{pkgname}={pkgver}-r{pkgrel}"]
    self.install_if = [f"{pkgname}={pkgver}-r{pkgrel}", "xinit"]
    return [
        "etc/X11/Xsession.d",
    ]

@subpackage("dinit-chimera-links")
def _def(self):
    self.pkgdesc = f"{pkgdesc} (service links)"
    self.depends = [f"{pkgname}={pkgver}-r{pkgrel}"]
    self.install_if = [f"{pkgname}={pkgver}-r{pkgrel}"]
    self.options = ["brokenlinks"]
    return [
        "usr/lib/dinit.d/boot.d/agetty-*"
    ]
