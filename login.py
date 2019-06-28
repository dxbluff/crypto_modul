#!/usr/bin/python3.6
import os
import mount 
import crypt


if __name__ == "__main__":
    user=mount.getuser()
    key = crypt.hash((os.environ['TOKEN']).encode())
    
    if os.path.exists("/home/osboxes/algebra/Disks/{}.img.enc".format(user)):
        crypt.decrypt_file(key, '/home/osboxes/algebra/Disks/{}.img.enc'.format(user))        
        mount.mount('/home/osboxes/algebra/Disks/{}.img'.format(user))
    else:
        vhd=mount.createVHD(user)
        VHD_MOUNT_POINT=mount.mount(vhd)
    exit()
