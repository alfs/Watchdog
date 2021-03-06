#!/usr/bin/env

import os
import pwd
import grp
import sys
import time
from subprocess import STDOUT, check_output, CalledProcessError

MAINT_DIR="/monroe/maintenance"
MAINT_USER="monroe"
MAINT_FLAG="/monroe/maintenance/enabled"
MAINT_FLAG_LEGACY="/.maintenance"
MAINT_FILE="/monroe/maintenance/reason"

def trigger_maintenance(reason):
    if not os.path.exists(MAINT_DIR):
        os.makedirs(MAINT_DIR)
    os.chmod(MAINT_DIR,0o777)

    uid = pwd.getpwnam(MAINT_USER).pw_uid
    gid = grp.getgrnam(MAINT_USER).gr_gid
    
    try:
        fd = open(MAINT_FLAG,"w")
        fd.write("1\n")
        fd.close()
    except Exception,ex:
    	print ex
    	pass

    try:
        os.chown(MAINT_FLAG,uid,gid)
        os.symlink(MAINT_FLAG,MAINT_FLAG_LEGACY)
    except Exception,ex:
    	print ex
    	pass

    try:
        fd = open(MAINT_FILE,"w")
        fd.write("[%s] %s\n" % (time.time(),reason))
        fd.close()
        os.chown(MAINT_FILE,uid,gid)
    except Exception,ex:
    	print ex
 
def trigger_reboot():
    ## DISABLED until tested
    ## shell("shutdown -r +1 'System self-test unrecoverable. Trying reboot in 1 min.'")
    ## sleep(300) # wait 5 min, then force reboot if we are still running.
    ## shell("echo 1 > /proc/sys/kernel/sysrq")
    ## shell("echo b > /proc/sysrq-trigger")
    pass

def trigger_reinstall():
    # TODO: remove the successful boot hint to cause reinstall
    # on boot

    ## DISABLED until reinstallation preserves key files
    ## shell("grub-editenv /.bootos set FORCEREINSTALL=1")
    #trigger_reboot()
    pass

def shell(cmd, timeout=10, source=None, bashEscape=False):
    if bashEscape:
        cmd = "timeout -s 9 %i bash -c '%s'" % (timeout, cmd)
    else:
        cmd = "timeout -s 9 %i %s" % (timeout, cmd)
    if source:
        cmd = ". %s && %s" % (source, cmd)
    print "Running: %s" % cmd
    try:
      env = os.environ.copy()
      env['PATH']='/usr/bin/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
      output = check_output(cmd, stderr=STDOUT, shell=True, env=env)
    except OSError,er:
      output = str(er)
    except CalledProcessError,er:
      output = er.output
    except Exception,ex:
      print "[DEBUG]", ex
      output = "Failed"
    return output
