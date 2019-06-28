import os
import crypt

def createVHD(user):
    os.system('dd if=/dev/zero of=/home/osboxes/algebra/Disks/{}.img bs=1M count=120'.format(user))
    os.system('mkfs -t ext4 /home/osboxes/algebra/Disks/{}.img'.format(user))
    return '/home/osboxes/algebra/Disks/{}.img'.format(user)

def mount(path):
    var=os.popen('udisksctl loop-setup -f {}'.format(path)).read()
    dest=var.split(' ')[4].split('.')[0]
    os.environ["VHD_MOUNT_POINT"] = dest
    with open('/home/osboxes/algebra/Disks/.mount_point', "w") as outfile:
        outfile.write(dest)  
    return dest    
    
def unmount(path):
    os.system('udisksctl unmount -b {} '.format(path))        

def getuser():
    user=os.popen('whoami').read()
    user=user.split()[0]
    return user
