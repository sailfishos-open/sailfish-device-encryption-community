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


## Enabling device encryption

To make some device available for encryption, you should add INI
configuration file `devices.ini` in
`/etc/sailfish-device-encryption-community` folder. Typically, it
should be done by porter of the device through device configuration
repository (sparse in config). Format described through example below:

```INI
[home_device]
name=Home
device=/dev/mapper/sailfish-home
mapper=home_encrypted
mount=/home
type=device

[home_in_file]
name=Home
device=/encrypted.img
mapper=home_encrypted_file
mount=/home
type=file
size_mb=10240
```