# FIXME: cross support, check

from cbuild.core import chroot

def do_configure(self):
    self.do(
        "python3", self.configure_script, "configure",
        "--prefix=/usr", "--libdir=/usr/lib", *self.configure_args,
        env = self.configure_env
    )

def do_build(self):
    self.do(
        "python3", self.configure_script, "build", f"-j{self.make_jobs}",
        *self.make_build_args,
        env = self.make_build_env
    )

def do_check(self):
    pass

def do_install(self):
    self.do(
        "python3", self.configure_script, "install",
        "--destdir=" + str(self.chroot_destdir),
        *self.make_install_args,
        env = self.make_install_env
    )

def use(tmpl):
    tmpl.do_configure = do_configure
    tmpl.do_build = do_build
    tmpl.do_check = do_check
    tmpl.do_install = do_install

    tmpl.build_style_defaults = [
        ("configure_script", "waf"),
    ]