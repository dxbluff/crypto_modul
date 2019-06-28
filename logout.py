import mount
import crypt
import os

if __name__ == "__main__":    
    with open('/home/osboxes/algebra/Disks/.mount_point', "r") as outfile:
        VHD_MOUNT_POINT=outfile.read()
    print(VHD_MOUNT_POINT)
    mount.unmount(VHD_MOUNT_POINT)
    user = mount.getuser()
    key = crypt.hash((os.environ['TOKEN']).encode())
    crypt.encrypt_file(key, "/home/osboxes/algebra/Disks/{}.img".format(user))
    os.remove("/home/osboxes/algebra/Disks/{}.img".format(user))
    os.remove("/home/osboxes/algebra/Disks/.mount_point")
#    os.system("shutdown now")
