Name:       sailfish-device-encryption-community

Summary:    Sailfish Device Encryption Community
Version:    1.0
Release:    1
License:    GPLv2
URL:        https://github.com/rinigus/sailfish-device-encryption-community
Source0:    %{name}-%{version}.tar.bz2

BuildArch:  noarch

Requires:   cryptsetup
Requires:   systemd-ask-password-gui
Requires:   sailfish-device-encryption-community-wizard
Requires:   sailfish-device-encryption-community-settings
Requires:   sailfish-device-encryption-community-service
Requires:   sailfish-device-encryption-community-generator
Requires:   shadow-utils
Requires:   libargon2-tools

BuildRequires: pkgconfig(sailfishapp) >= 1.0.2
BuildRequires: cmake

%description
Support for storage encryption on SailfishOS. This is a community version.

%package droid
Summary:    Droid based device support for %{name}
Requires:   %{name} = %{version}

%description droid
Additional configuration for Hybris devices. Support for %{name}

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}

# system wide units
mkdir -p %{buildroot}%{_unitdir}
install -t %{buildroot}%{_unitdir} --mode=644 systemd/late-mount-pre.target
install -t %{buildroot}%{_unitdir} --mode=644 systemd/late-mount-post.target
install -t %{buildroot}%{_unitdir} --mode=644 systemd/late-mount.target
install -t %{buildroot}%{_unitdir} --mode=644 systemd/systemd-ask-password-gui.service
install -t %{buildroot}%{_unitdir} --mode=644 systemd/systemd-ask-password-gui.path
install -t %{buildroot}%{_unitdir} --mode=644 systemd/systemd-ask-password-gui-stop.service
install -t %{buildroot}%{_unitdir} --mode=644 systemd/sailfish-device-encryption-community-wizard.service
cp -r systemd/*.requires %{buildroot}%{_unitdir}
cp -r systemd/*.d %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_libexecdir}/sailfish-device-encryption-community
install -t %{buildroot}%{_libexecdir}/sailfish-device-encryption-community libexec/decrypt
install -t %{buildroot}%{_libexecdir}/sailfish-device-encryption-community libexec/hwcrypt-key
install -t %{buildroot}%{_libexecdir}/sailfish-device-encryption-community libexec/hwcrypt-key-generate
install -t %{buildroot}%{_libexecdir}/sailfish-device-encryption-community libexec/make-salt
install -t %{buildroot}%{_libexecdir}/sailfish-device-encryption-community libexec/mount-tmp

%post
getent group encryption-hwcrypt >/dev/null || groupadd -r encryption-hwcrypt
getent passwd encryption-hwcrypt >/dev/null || \
    useradd -r -g encryption-hwcrypt -b /var/empty --no-create-home -s /sbin/nologin \
    -c "Sailfish Encryption HWCrypt" encryption-hwcrypt

%files
%defattr(-,root,root,-)
%{_libexecdir}
%{_unitdir}/*.target
%{_unitdir}/*.service
%{_unitdir}/*.path
%{_unitdir}/*.requires


%files droid
%defattr(-,root,root,-)
%{_unitdir}/*.d/10-droid.conf
