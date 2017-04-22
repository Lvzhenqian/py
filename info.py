import subprocess

p = subprocess.Popen('ipconfig',
                     shell=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                     stdin=subprocess.DEVNULL,universal_newlines=True)
metric = p.stdout.read()