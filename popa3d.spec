%define name    popa3d
%define version 1.0.2

%define section Networking/Mail
%define summary Tiny POP3 daemon

Summary:        %summary
Name:           %name
Version:        %version
Release:        %mkrel 1
License:        BSD
Group:          Networking/Mail
URL:            http://www.openwall.com/popa3d/
Source0:        %name-%version.tar.bz2
Source1:	popa3d-xinet
Source2:	popa3d-pam
Patch0:		popa3d-params.patch
Patch1:		popa3d-0.6.4.patch
#Patch2:		popa3d-ipv6.patch.bz2
Patch3:		popa3d-maildir.patch
Patch4:		popa3d-vname.patch
Requires(pre):	rpm-helper
BuildRoot:      %_tmppath/%name-buildroot
Buildrequires:	pam-devel
Requires:	xinetd

%description
popa3d is a tiny POP3 daemon designed with security as the primary goal.

%prep
%setup -q
%patch0 -p0 -b .popa3d-params
%patch1 -p0 -b .popa3d-log_ip
#%patch2 -p0 -b .popa3d-ipv6
%patch3 -p0 -b .popa3d-maildir
%patch4 -p0 -b .popa3d-vname

%build
%make LIBS="-lpam -lcrypt"

%install
rm -rf %buildroot

%__install -d $RPM_BUILD_ROOT%_var/empty
%__install -d $RPM_BUILD_ROOT%_sysconfdir/xinetd.d && \
%__install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%_sysconfdir/xinetd.d/popa3d
%__install -d $RPM_BUILD_ROOT%_sysconfdir/pam.d && \
%__install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%_sysconfdir/pam.d/popa3d

%makeinstall PREFIX=$RPM_BUILD_ROOT \
		SBINDIR=$RPM_BUILD_ROOT%{_sbindir} \
		MANDIR=$RPM_BUILD_ROOT%{_mandir}

%pre
%_pre_useradd popa3d /var/empty /bin/false

%postun
%_postun_userdel popa3d

%clean
rm -rf %buildroot

%files
%defattr(644,root,root,755)
%doc LICENSE INSTALL DESIGN CHANGES CONTACT VIRTUAL
%dir %_var/empty
%config(noreplace) %_sysconfdir/xinetd.d/popa3d
%config(noreplace) %_sysconfdir/pam.d/popa3d
%_mandir/man8/*
%defattr(755,root,root)
%_sbindir/*


