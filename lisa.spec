Summary:	The LAN Information Server
Summary(pl):	Serwer informacji o LANie
Name:		lisa
Version:	0.2.1
Release:	2
License:	GPL
Group:		Daemons
Source0:	http://lisa-home.sourceforge.net/src/lisa-0.2.1.tar.bz2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-acam.patch
Patch1:		%{name}-net_auto_conf.patch
Patch2:		%{name}-default_config.patch
URL:		http://lisa-home.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
PreReq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LISa is a small daemon which is intended to run on end user systems. It
provides something like a "network neighbourhood", but only relying on
the TCP/IP protocol stack, no smb or whatever.

%description -l pl
LISA jest ma³ym daemonem przeznaczonym do dzia³ania na komputerach
u¿ytkowników. Dostarcza czego¶ w rodzaju ,,Otoczenia Sieciowego'' ale
bazuj±c jedynie na protokole TCP/IP a nie na SMB.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
rm -f missing
%{__libtoolize}
aclocal
%{__autoconf}
autoheader
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}

install lisa/lisarc $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/lisa
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/lisa

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add lisa
if [ -r /var/lock/subsys/lisa ]; then
	/etc/rc.d/init.d/lisa restart >&2
else
	echo "Run \"/etc/rc.d/init.d/lisa start\" to start Lisa daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/lisa ]; then
		/etc/rc.d/init.d/lisa stop >&2
	fi
	/sbin/chkconfig --del lisa
fi

%files
%defattr(644,root,root,755)
%doc README NEWS AUTHORS ChangeLog
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/lisarc
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/lisa
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/lisa
