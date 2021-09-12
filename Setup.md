# Enabling device encryption

Enabling device encryption is expected to be done by porter of the
device. Below, the steps required for it are listed.

## Support for hardware assisted encryption (recommended)

While it is not required, it is recommended to enable hardware
assisted encryption support if it is available for your
device. Currently,
[hwcrypt](https://github.com/sailfishos-open/hwcrypt) is supported but
it should be possible to extend support to other hardware assisted
options if they are available. HWCrypt is using hardware-bound key for
generation of LUKS password from the user input.

For hybris-based ports, see
[hwcrypt](https://github.com/sailfishos-open/hwcrypt) for compilation
instructions. Include generated package into your droid-hal packages.

Next, add
```
Requires: droid-hwcrypt
```
into your patterns (droid-config).


## Required packages

Add `libargon2`, this project, and all sub-projects to your image
build. Easiest is to use OBS and copy the following packages from Tama
port:

- https://build.sailfishos.org/package/show/nemo:devel:hw:sony:tama:aosp10/libargon2
- https://build.sailfishos.org/package/show/nemo:devel:hw:sony:tama:aosp10/libsfosdevenc
- https://build.sailfishos.org/package/show/nemo:devel:hw:sony:tama:aosp10/sailfish-device-encryption-community
- https://build.sailfishos.org/package/show/nemo:devel:hw:sony:tama:aosp10/sailfish-device-encryption-community-service
- https://build.sailfishos.org/package/show/nemo:devel:hw:sony:tama:aosp10/sailfish-device-encryption-community-settings
- https://build.sailfishos.org/package/show/nemo:devel:hw:sony:tama:aosp10/sailfish-device-encryption-community-wizard
- https://build.sailfishos.org/package/show/nemo:devel:hw:sony:tama:aosp10/systemd-ask-password-gui

I hope that these packages can later be pushed into "common"
repositories (devel and testing) making this step unnecessary.

To include packages into the build, add
```
Requires: sailfish-device-encryption-community
```
into your patterns (droid-config).


## Changes in droid-config

To make some device available for encryption, you should add INI
configuration file `devices.ini` in
`/etc/sailfish-device-encryption-community` folder. It is expected
that this is done through changes in "sparse" of droid-config.

The configuration would depend on whether you have LVM-based port or
you have the same partition for `/home` and `/`, as it is for
LineageOS based ports.


### Configuration file

System setup is described through `devices.ini`. In this file, list of
devices is given with each of them having storage (file or partition),
mountpoint, and the state. If no state is given (keyword `state`) or
it is not recognized then it is assumed that device requires a reset
as during the first boot. So, in the following instructions, `state`
is left out accordingly.

Usually, it is expected that only one device is configured and set to
be `/home` mountpoint. Note that this solution does not support
encryption of `/` as mounting happens at the later boot stages.

As a general comment, to avoid `-` mangling by device mapper, it is
better to use `_` when composing device names. This approach was used
in the suggested configuration below.


### Configuration for ports with `/home` on `/` partition

If there is no separate partition for `/home` then the configuration
is easier and limited by addition of a single `devices.ini` file:

```INI
[home_in_file]
name=Home
device=/encrypted.img
mapper=home_encrypted_file
mount=/home
type=file
size_mb=10240
```

During the first boot, file `/encrypted.img` will be created by the
wizard if the user will request encrypted `/home` partition. This
configuration would allocate `10240 MB` for `/home`. Similar to
LVM-based ports, you would have to decide how much to allocate for
`/home` and how much to leave for remaining files in `/`.

If no encryption is requested then whole setup should work as before
without encryption. No file is created and `/home` will be a part of
`/` partition. If file `/encrypted.img` exists then it will be removed
by the wizard while resetting the device. 


### Configuration for ports with separate `/home` partition

For ports using LVM and with separate `/home` partition, there are a
bit more changes that have to be done due to the coupling of LUKS
password and device security code (PIN). See corresponding
[issue](https://forum.sailfishos.org/t/allow-to-decouple-luks-password-from-used-security-code)
for background. As this issue influences configuration in several
packages, "PINgate" is used to refer to it.

As a result, we cannot use `/dev/sailfish/home` and have to use some
other partition name. In the following, `/dev/sailfish/home_open` is
suggested.

As for file-based approach, `devices.ini` is needed:

```INI
[home_device]
name=Home
device=/dev/sailfish/home_open
mapper=home_encrypted
mount=/home
type=device
```

Next, we need to remove `/home` from `fstab`. This can be achieved by
adjusting hybris `pack` script as shown below:

```DIFF
diff --git a/kickstart/pack/h8216/hybris b/kickstart/pack/h8216/hybris
index d199c10..aa47dd5 100644
--- a/kickstart/pack/h8216/hybris
+++ b/kickstart/pack/h8216/hybris
@@ -21,9 +21,11 @@ fi
 RELEASENAME=${NAME// /_}-${SAILFISH_CUSTOMER// /_}${SAILFISH_CUSTOMER:+-}${EXTRA_NAME// /_}$RND_FLAVOUR${RND_FLAVOUR:+-}$VERSION_ID$DEVICE_ID
 
 # Remove /opt mounting from fstab, systemd will handle it
+# Remove /home mounting from fstab, it is handled through encryption scripts
 mkdir root
 mount -o loop root.img root
 sed -i '/\/opt/d' root/etc/fstab
+sed -i '/\/home/d' root/etc/fstab
 umount root
 rm -rf root
```

Then, due to PINgate issue, `home_open` has to be created instead of
`home`:

```DIFF
diff --git a/kickstart/pack/h8216/hybris b/kickstart/pack/h8216/hybris
index aa47dd5..5696a82 100644
--- a/kickstart/pack/h8216/hybris
+++ b/kickstart/pack/h8216/hybris
@@ -91,14 +91,14 @@ echo "Create logical volume ROOT size: $ROOTSIZE"
 /usr/sbin/lvcreate -L ${ROOTSIZE}B --name root sailfish
 
 echo "Create logical volume HOME size: $HOMESIZE"
-/usr/sbin/lvcreate -L ${HOMESIZE}B --name home sailfish
+/usr/sbin/lvcreate -L ${HOMESIZE}B --name home_open sailfish
 
 /bin/sync
 /usr/sbin/vgchange -a y sailfish
 
 dd if=root.img bs=$BLOCKSIZE count=$ROOTBLOCKS of=/dev/sailfish/root
 
-dd if=home.img bs=$BLOCKSIZE count=$HOMEBLOCKS of=/dev/sailfish/home
+dd if=home.img bs=$BLOCKSIZE count=$HOMEBLOCKS of=/dev/sailfish/home_open
 
 /usr/sbin/vgchange -a n sailfish
```

See example pack script at [Tama
port](https://github.com/sailfishos-sony-tama/droid-config-sony-tama-pie/blob/hybris-10/kickstart/pack/h8216/hybris)
with the required changes.

### hwcomposer-2-3

For devices using `hwcomposer-2-3`, add `/etc/systemd/system/systemd-ask-password-gui-stop.service.d/50-vendor-hwcomposer-2-3.conf` into the sparse of droid-config:
```
[Service]
ExecStartPre=-/usr/bin/killall systemd-ask-password-gui
# stop first in case something else managed to start it
ExecStartPre=-/system/bin/stop vendor.hwcomposer-2-3
ExecStartPre=-/system/bin/start vendor.hwcomposer-2-3
ExecStart=/bin/echo After vendor.hwcomposer-2-3 restart
```

Without such restart of hwcomposer, Jolla Sailfish Setup will not be
able to recognize touchscreen events and there could be issues with
the showing setup windows as well.


### Factory image (devices with separate /home partition)

On Tama, factory image was removed leading to reduction of the
generated image by the factor of 2. In addition, the partition that
has been used for storing factory images can be used to extend PV of
LVM storage.

To disable factory image creation and addition to the generated ZIP,
you would have to make changes in your droid-config:

- add `Provides: jolla-settings-system-reset` to your droid-config
  meta patterns.

- commenting out image creation and removal of temporary files in
  kickstart pack script. See implementation for Tama at
  [pack/hybris](https://github.com/sailfishos-sony-tama/droid-config-sony-tama-pie/blob/hybris-10/kickstart/pack/h8216/hybris)

- remove creation of fimage partition in kickstart/part. See
  [example](https://github.com/sailfishos-sony-tama/droid-config-sony-tama-pie/blob/hybris-10/kickstart/part/h8216)

- remove fimage from flash scripts. Examples at
  [flash.sh](https://github.com/sailfishos-sony-tama/droid-config-sony-tama-pie/blob/hybris-10/sparse/boot/flash.sh)
  and
  [flash-on-windows.bat](https://github.com/sailfishos-sony-tama/droid-config-sony-tama-pie/blob/hybris-10/sparse/boot/flash-on-windows.bat).

If it is preferred to keep factory image generation and flashing then
you would have to investigate which scripts would have to be modified
to ensure that the factory reset works as it should.


## nemo-qml-plugin-systemsettings (devices with separate /home partition)

Changes in this section are required for devices with separate `/home`
partition only and are induced by [PINgate
issue](https://forum.sailfishos.org/t/allow-to-decouple-luks-password-from-used-security-code).

As Settings/Storage will now start showing `/dev/sailfish/home_open`
as an encrypted SD card, we have to patch
nemo-qml-plugin-systemsettings using
https://github.com/sailfishos/nemo-qml-plugin-systemsettings/pull/7.

Without this patch user will be shown actions such as "Format" for
that partition without any indication that it is storing `/home`.


## hybris-initrd and droid-hal-img-boot (devices with separate /home partition)

As LVM partition is resized on the first boot, initrd needs to know
its name. Due to PINgate, the changes are needed in hybris-initrd to
set the name of home partition:

```DIFF

diff --git a/sbin/root-mount b/sbin/root-mount
index 0554d95..fcd9409 100755
--- a/sbin/root-mount
+++ b/sbin/root-mount
@@ -54,7 +54,7 @@ if test -z "$PHYSDEV"; then
 fi
 
 ROOTDEV="/dev/sailfish/root"
-HOMEDEV="/dev/sailfish/home"
+HOMEDEV="/dev/sailfish/home_open"
 MOUNT_POINT=$1
 
 LVM_RESERVED_KB=$(expr $LVM_RESERVED_MB \* 1024)
```

See https://github.com/sailfishos-sony-tama/hybris-initrd/commit/10dd2f1b54d4feba0ede523aaac15f30ffc2d31d .

After making the changes, pull updated hybris-initrd into droid-hal-img-boot.
