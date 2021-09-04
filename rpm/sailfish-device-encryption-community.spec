Name:       sailfish-device-encryption-community

Summary:    Sailfish Device Encryption Community
Version:    0.1
Release:    1
License:    GPLv2
URL:        https://github.com/rinigus/sailfish-device-encryption-community
Source0:    %{name}-%{version}.tar.bz2

BuildArch:  noarch

Requires:   cryptsetup
Requires:   systemd-ask-password-gui
Requires:   sailfish-device-encryption-community-wizard
Requires:   shadow-utils
Requires:   libargon2-tools

%description
Support for storage encryption on SailfishOS. This is a community version.

%prep

%build

%install
rm -rf %{buildroot}

# system wide units
mkdir -p %{buildroot}/%{_unitdir}
install -t %{buildroot}/%{_unitdir} --mode=644 systemd/late-mount.target
install -t %{buildroot}/%{_unitdir} --mode=644 systemd/systemd-ask-password-gui.service
install -t %{buildroot}/%{_unitdir} --mode=644 systemd/systemd-ask-password-gui-stop.service
cp -r systemd/*.requires %{buildroot}/%{_unitdir}
cp -r systemd/*.wants %{buildroot}/%{_unitdir}

mkdir -p %{buildroot}/%{_libexecdir}/sailfish-device-encryption-community
install -t %{buildroot}/%{_libexecdir}/sailfish-device-encryption-community libexec/decrypt
install -t %{buildroot}/%{_libexecdir}/sailfish-device-encryption-community libexec/hwcrypt-key
install -t %{buildroot}/%{_libexecdir}/sailfish-device-encryption-community libexec/hwcrypt-key-generate
install -t %{buildroot}/%{_libexecdir}/sailfish-device-encryption-community libexec/make-salt

# config units - remove later from here
mkdir -p %{buildroot}/%{_sysconfdir}/systemd/system
cp -r etc/* %{buildroot}/%{_sysconfdir}/systemd/system

%post
getent group encryption-hwcrypt >/dev/null || groupadd -r encryption-hwcrypt
getent passwd encryption-hwcrypt >/dev/null || \
    useradd -r -g encryption-hwcrypt -b /var/empty --no-create-home -s /sbin/nologin \
    -c "Sailfish Encryption HWCrypt" encryption-hwcrypt

%files
%defattr(-,root,root,-)
%{_unitdir}
%{_libexecdir}
%{_sysconfdir}
