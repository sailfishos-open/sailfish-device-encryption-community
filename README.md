# Support for device storage encryption

This is a community edition for enabling encryption on Sailfish
OS. Encryption of /home is targeted and can be achieved for ports
using the same approach as official ports (home in LVM) as well as
ports based on LineageOS. For latter, a file encrypted by LUKS and
made available through device mapper when unlocking it can be
formatted and used as /home.

Compared to the official encryption solution, this edition has way
larger flexibility in LUKS passwords which has a major implication in
the security. As it is, official encryption solution is vulnerable to
brute force attack. Such attack can be rendered unfeasible using this
community edition.

Project consists of several packages:

- [sailfish-device-encryption-community](https://github.com/sailfishos-open/sailfish-device-encryption-community):
  this repository with SystemD units and other scripts. Provides main
  RPM that pulls in all required dependencies.

- [wizard](https://github.com/sailfishos-open/sailfish-device-encryption-community-wizard):
  Wizard used to setup device on the first boot with or without
  encryption, as preferred by the user.

- [systemd-ask-password-gui](https://github.com/sailfishos-open/systemd-ask-password-gui):
  GUI for entering password during a boot.

- [service](https://github.com/sailfishos-open/sailfish-device-encryption-community-service):
  Support service allowing to change device encryption passwords and
  obtain some information regarding encrypted devices. 

- [settings](https://github.com/sailfishos-open/sailfish-device-encryption-community-settings):
  GUI in Sailfish Settings for encrypted devices.

- [generator](https://github.com/sailfishos-open/sailfish-device-encryption-community-generator):
  SystemD generator used to create unit files on boot.

- [libsfosdevenc](https://github.com/sailfishos-open/libsfosdevenc):
  Support library used by the wizard and the service to handle
  encryption of the devices.

- [hwcrypt](https://github.com/sailfishos-open/hwcrypt): Hardware
  assisted encryption of the password. Recommended on Android-based
  devices.


## Issues

Please file issues to all sub-projects in this repository, at
[Issues](https://github.com/sailfishos-open/sailfish-device-encryption-community).


## Dependencies

Additional external dependencies are

- cryptsetup - provided by Sailfish core packages
- libargon2 - available as a library in Sailfish OS Chum


## How it works

This solution allows you to use alphanumeric passwords of any length,
passwords that are processed by hardware bound keys, and several
passwords for unlocking LUKS volumes. User can add and remove
passwords using System Setup to adjust to the particular requirements.

Password types are defined in supporting library and in the scripts
used to unlock the device. Approach is modular allowing us to extend
the password types in future through definition of new password
classes and adjusting the scripts used during the boot.

Encryption support is ensured through combination of services and
interaction with systemd-provided facilities. On the first boot,
wizard will ask user to select whether encryption is desired or
not. Note that at this stage, device in question will be formatted
(with or without) removing all the data if it was there. However, as
it is expected to be done on fresh install, no data loss
expected. After the wizard will finish its work, reboot will be
performed by user.

After reboot, encrypted devices will have to be mounted and Jolla
Setup can proceed. In this case, boot sequence for encryption
subsystem is the same as during normal boot.

### Recovery password

On setup, recovery password is generated and its copy is saved in the
encrypted filesystem. It is recommended to copy the password away from
the device and remove its copy from the filesystem. For that, use
System Settings/Encryption to access the recovery password and remove
its copy.

After removal of the copy, the recovery password will be impossible to
show in the settings.

To use recovery password, enter it as it is with all dashes using
"Plain text" password type.

### Boot sequence

Encryption is supported by adding three systemd boot targets:
- late-mount-pre
- late-mount
- late-mount-post

All these targets are ordered after `basic` target and in the order as
given above. `late-mount-pre` is used by wizard to ensure that it is
possible to reset the devices if requested.

`late-mount` is the target where the encrypted devices are opened and
mounted. For that, decryption scripts ask for encryption password(s)
using systemd-ask-password and get the response through
`systemd-ask-password-gui`.

`late-mount-post` is used to cleanup the state of the device. Namely,
`systemd-ask-password-gui` is killed to avoid interference with the
GUI apps used later in the boot process (Lipstick, Jolla Setup).

`late-mount-post` is set as a requirement for `multi-user` target and
`systemd-user-sessions`.

Mount units and decryption services are generated based on the setup
automatically via wizard.

### Passwords

Currently, plain text and `hwcrypt`-based hardware assisted passwords
are supported. Plain text password is forwarded to cryptsetup as
it is.

Hardware assisted password is generated by first applying salt using
`libargon2` and then signing with RSA using `hwcrypt` through
hardware-bound key. As a result, LUKS can be opened on the device only
which allows users to use simpler (but not trivial) passwords than in
the plain text password case.


## Setup

Setup is described separately in [Setup.md](Setup.md).