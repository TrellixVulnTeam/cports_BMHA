pkgname = "syslog-ng"
pkgver = "3.38.1"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--sysconfdir=/etc/syslog-ng",
    "--with-ivykis=system",
    "--with-jsonc=system",
    "--with-librabbitmq-client=system",
    "--disable-systemd",
    "--disable-mongodb",
    "--disable-riemann",
    "--disable-geoip2",
    "--disable-smtp",
    "--disable-java",
    "--disable-java-modules",
    "--disable-linux-caps",
    "--enable-extra-warnings",
    "--enable-manpages",
    "--enable-native",
    "--enable-python",
    "--enable-ipv6",
    "--enable-redis",
    "--enable-stomp",
    "--enable-amqp",
    "--enable-json",
    "--enable-http",
    "--enable-sql",
]
make_cmd = "gmake"
make_install_args = ["-j1"]
hostmakedepends = [
    "pkgconf", "gmake", "flex", "bison", "file", "python", "glib-devel",
]
makedepends = [
    "libcurl-devel", "python-devel", "pcre-devel", "openssl-devel",
    "eventlog-devel", "libglib-devel", "hiredis-devel", "ivykis-devel",
    "libdbi-devel", "json-c-devel", "rabbitmq-c-devel"
]
pkgdesc = "Next generation logging daemon"
maintainer = "q66 <q66@chimera-linux.org>"
license = "LGPL-2.1-or-later AND GPL-2.0-or-later"
url = "https://www.syslog-ng.com/products/open-source-log-management"
source = f"https://github.com/{pkgname}/{pkgname}/releases/download/{pkgname}-{pkgver}/{pkgname}-{pkgver}.tar.gz"
sha256 = "5491f686d0b829b69b2e0fc0d66a62f51991aafaee005475bfa38fab399441f7"
# tests need https://github.com/Snaipe/Criterion
options = ["!check"]

def init_configure(self):
    self._pyver = self.do(
        "pkgconf", "--modversion", "python3", capture_output = True
    ).stdout.decode().strip()

def post_install(self):
    # service file
    self.install_service(self.files_path / "syslog-ng")

    # taken from Alpine
    self.rm(self.destdir / "etc/syslog-ng/syslog-ng.conf")
    self.install_file(self.files_path / "syslog-ng.conf", "etc/syslog-ng")

    sitepkgs = f"usr/lib/python{self._pyver}/site-packages"
    self.install_dir(sitepkgs)

    # move python bindings into the correct place
    for f in (self.destdir / "usr/lib/syslog-ng/python").iterdir():
        self.mv(f, self.destdir / sitepkgs)

    # getent module will not work correctly on musl as musl does
    # not provide reentrant getprotoby(name|number)
    self.rm(self.destdir / "usr/lib/syslog-ng/libtfgetent.so")

@subpackage("syslog-ng-scl")
def _scl(self):
    self.pkgdesc = f"{pkgdesc} (configuration library)"

    return ["usr/share/syslog-ng/include/scl"]

@subpackage("syslog-ng-devel")
def _devel(self):
    return self.default_devel(extra = [
        "usr/share/syslog-ng/tools",
        "usr/share/syslog-ng/xsd",
    ])

@subpackage("syslog-ng-python")
def _python(self):
    self.pkgdesc = f"{pkgdesc} (python module)"

    return [
        "usr/lib/syslog-ng/libmod-python.so",
        "usr/lib/python*",
    ]

def _genmod(modn, modl):
    @subpackage(f"syslog-ng-{modn}_module")
    def _mod(self):
        nonlocal modn, modl

        self.pkgdesc = f"{pkgdesc} ({modn} module)"

        if not modl:
            modl = modn

        return [f"usr/lib/syslog-ng/lib{modl}.so"]

for modn, modl in [
    ("add-contextual-data", None),
    ("amqp", "afamqp"),
    ("examples", None),
    ("graphite", None),
    ("http", None),
    ("json", "json-plugin"),
    ("map-value-pairs", None),
    ("redis", None),
    ("sql", "afsql"),
    ("stardate", None),
    ("stomp", "afstomp"),
    ("tags-parser", None),
    ("xml", None),
]:
    _genmod(modn, modl)
