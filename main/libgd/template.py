pkgname = "libgd"
# TODO: 2.3.3 fails tests
pkgver = "2.3.2"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--without-xpm"]
hostmakedepends = ["pkgconf"]
makedepends = [
    "libjpeg-turbo-devel", "libpng-devel", "libwebp-devel",
    "libtiff-devel", "fontconfig-devel",
    # TODO: other image formats (heif, avif, ...)
]
checkdepends = ["fonts-liberation-otf"]
pkgdesc = "Graphics library for the dynamic creation of images"
maintainer = "q66 <q66@chimera-linux.org>"
license = "custom:libgd"
url = "https://libgd.github.io"
source = f"https://github.com/{pkgname}/{pkgname}/releases/download/gd-{pkgver}/{pkgname}-{pkgver}.tar.xz"
sha256 = "478a047084e0d89b83616e4c2cf3c9438175fb0cc55d8c8967f06e0427f7d7fb"

def post_install(self):
    self.install_license("COPYING")

@subpackage("libgd-static")
def _static(self):
    return self.default_static()

@subpackage("libgd-devel")
def _devel(self):
    return self.default_devel(man = True)

@subpackage("libgd-progs")
def _xmlwf(self):
    self.depends += ["perl"]

    return self.default_progs()