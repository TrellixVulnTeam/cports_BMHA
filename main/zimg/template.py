pkgname = "zimg"
pkgver = "3.0.4"
pkgrel = 0
build_style = "gnu_configure"
hostmakedepends = ["pkgconf", "automake", "libtool"]
makedepends = ["linux-headers"] # hwcap on arm etc.
pkgdesc = "Image processing library"
maintainer = "q66 <q66@chimera-linux.org>"
license = "WTFPL"
url = "https://github.com/sekrit-twc/zimg"
source = f"{url}/archive/release-{pkgver}.tar.gz"
sha256 = "219d1bc6b7fde1355d72c9b406ebd730a4aed9c21da779660f0a4c851243e32f"

def pre_configure(self):
    self.do(self.chroot_cwd / "autogen.sh")

def post_install(self):
    self.install_license("COPYING")

@subpackage("zimg-devel")
def _devel(self):
    return self.default_devel()
