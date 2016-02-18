#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class MarvinFinal:
    """Reboot"""

    def run(self):
        return trigger_reboot()

class RestartMarvin:
    """enable & restart marvin service"""
    def run(self):
        shell("systemctl enable marvind")
        shell("systemctl restart marvind")

class ReinstallMarvin:
    """reinstall marvin service"""

    def run(self):
        shell("apt-get install -y --force-yes --reinstall python-marvin", timeout=60)

class MarvinService (module.BasicModule):
    """marvin service"""

    repairs = [RestartMarvin(), ReinstallMarvin()]
    final   = MarvinFinal()

    def run(self):
        # is marvin running
        ps =  shell("ps ax|grep marvind")
        if not "marvind.py" in ps: 
            return False
        # is it a service? 
        status =  shell("systemctl status marvind")
        if not "running" in status: 
            return False
        return True

register.put(MarvinService())
