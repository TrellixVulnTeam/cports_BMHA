pkgname = "base-files"
pkgver = "0.1"
pkgrel = 0
build_style = "meta"
pkgdesc = "Chimera Linux base system files"
maintainer = "q66 <q66@chimera-linux.org>"
license = "custom:meta"
url = "https://chimera-linux.org"
# no tests
options = ["!check", "bootstrap", "keepempty", "brokenlinks"]

def do_install(self):
    # base root dirs
    for d in [
        "boot", "etc", "etc/modprobe.d", "etc/modules-load.d",
        "home", "dev", "proc", "usr", "mnt", "opt", "sys", "media", "var",
        "run", "run/lock"
    ]:
        self.install_dir(d)

    # /usr dirs
    for d in [
        "local", "local/bin", "local/sbin", "local/include", "local/lib",
        "bin", "include", "lib", "src"
    ]:
        self.install_dir("usr/" + d)

    # /usr/share and /usr/local/share
    for d in [
        "locale", "misc", "terminfo", "zoneinfo", "doc", "info"
    ]:
        self.install_dir("usr/share/" + d)
        self.install_dir("usr/local/share/" + d)

    # apk exec dir
    self.install_dir("usr/lib/apk/exec")

    # mandirs
    for i in range(1, 9):
        self.install_dir("usr/share/man/man" + str(i))
        self.install_dir("usr/local/share/man/man" + str(i))

    # /var dirs
    for d in ["empty", "log", "opt", "cache", "lib", "mail", "spool"]:
        self.install_dir("var/" + d)

    # /var symlinks
    self.install_link("../run/lock", "var/lock")
    self.install_link("../run", "var/run")
    self.install_link("../mail", "var/spool/mail")

    # root's home dir
    self.install_dir("root")
    (self.destdir / "root").chmod(0o750)

    # /tmp and /var/tmp
    self.install_dir("tmp")
    (self.destdir / "tmp").chmod(0o777)
    self.install_dir("var/tmp")
    (self.destdir / "var/tmp").chmod(0o777)

    # Create bin and lib dirs and symlinks
    for d in ["bin", "lib"]:
        self.install_dir("usr/" + d)
        self.install_link("usr/" + d, d)

    # Symlink sbin paths to /usr/bin
    self.install_link("usr/bin", "sbin")
    self.install_link("bin", "usr/sbin")

    for f in [
        "profile", "hosts", "issue", "subuid", "subgid",
        "fstab", "passwd", "group", "securetty", "nsswitch.conf"
    ]:
        self.install_file(self.files_path / "etc" / f, "etc")

    # permissions for securetty
    (self.destdir / "etc/securetty").chmod(0o600)

    self.install_dir("etc/profile.d")

    for f in (self.files_path / "profile.d").glob("*.sh"):
        self.install_file(f, "etc/profile.d")

    # Install common licenses
    self.install_dir("usr/share/licenses")

    for f in (self.files_path / "licenses").iterdir():
        self.install_file(f, "usr/share/licenses")

    self.install_bin(self.files_path / "lsb_release")
    self.install_file(self.files_path / "os-release", "etc")

    # Create /proc/self/mounts -> /etc/mtab symlink
    self.install_link("/proc/self/mounts", "etc/mtab")

@subpackage("base-locale")
def _baseloc(self):
    self.pkgdesc = "Base package for locale data"
    self.depends = []
    self.build_style = "meta"

    return []

@subpackage("base-doc")
def _basedoc(self):
    self.pkgdesc = "Base package for documentation"
    self.depends = []
    self.build_style = "meta"

    return []
