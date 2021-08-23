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

%description
Support for storage encryption on SailfishOS. This is a community version.

%prep

%build

%install
rm -rf %{buildroot}

# system wide units
mkdir -p %{buildroot}/%{_unitdir}
install -t %{buildroot}/%{_unitdir} systemd/late-mount.target
install -t %{buildroot}/%{_unitdir} systemd/systemd-ask-password-gui.service
install -t %{buildroot}/%{_unitdir} systemd/systemd-ask-password-gui-stop.service
cp -r systemd/*.requires %{buildroot}/%{_unitdir}
cp -r systemd/*.wants %{buildroot}/%{_unitdir}

mkdir -p %{buildroot}/%{_libexecdir}/sailfish-device-encryption-community
install -t %{buildroot}/%{_libexecdir}/sailfish-device-encryption-community libexec/decrypt

# config units - remove later from here
mkdir -p %{buildroot}/%{_sysconfdir}/systemd/system
cp -r etc/* %{buildroot}/%{_sysconfdir}/systemd/system

%files
%defattr(-,root,root,-)
%{_unitdir}
%{_libexecdir}
%{_sysconfdir}
