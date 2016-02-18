#!/usr/bin/env python

from biteback import module, register
from biteback.util import shell, trigger_reboot

class AnsibleFinal:
    """Reinstall"""

    def run(self):
        return trigger_reinstall()

class RescheduleAnsible:
    """restore ansible cron entry"""
    def run(self):
        shell("crontab -l | grep -v ansible-wrapper | { cat; echo '42 * * * * /usr/bin/ansible-wrapper &>/dev/null' } | crontab")

class Ansible (module.BasicModule):
    """ansible wrapper installed in crontab"""

    repairs = [RescheduleAnsible()]
    final   = AnsibleFinal()

    def run(self):
        cron =  shell("crontab -l")
        if not "ansible-wrapper" in cron: 
            return False
        return True

register.put(Ansible())
