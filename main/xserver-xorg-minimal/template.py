pkgname = "xserver-xorg-minimal"
pkgver = "1.0"
pkgrel = 0
build_style = "meta"
depends = [
    "xserver-xorg-core", "xserver-xorg-input-libinput", "xauth", "xinit"
]
pkgdesc = "Minimal X.org metapackage"
maintainer = "q66 <q66@chimera-linux.org>"
license = "custom:meta"
url = "https://xorg.freedesktop.org"