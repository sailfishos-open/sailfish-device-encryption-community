# Support for device storage encryption

This is a community edition for enabling encryption on Sailfish
OS. Encryption of /home is targeted and can be achieved for ports
using the same approach as official ports (home in LVM) as well as
ports based on LineageOS. For latter, a file encrypted by LUKS and
made available through device mapper when unlocking it can be
formatted and used as /home.

Dependencies:
- cryptsetup
- [systemd-ask-password-gui](https://github.com/sailfishos-open/systemd-ask-password-gui)
- recommended for HW assisted encryption: [hwcrypt](https://github.com/sailfishos-open/hwcrypt)
