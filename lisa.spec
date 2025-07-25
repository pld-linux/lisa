Summary:	The LAN Information Server
Summary(pl.UTF-8):	Serwer informacji o LANie
Name:		lisa
Version:	0.2.2
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://lisa-home.sourceforge.net/src/%{name}-%{version}.tar.bz2
# Source0-md5:	cba116a4880f77205e0813d93bf14310
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	http://lisa-home.sourceforge.net/src/lslan-latest.tar.gz
# Source3-md5:	536b2382f92b6777e4e8fab022d4def8
Patch1:		%{name}-net_auto_conf.patch
Patch2:		%{name}-default_config.patch
URL:		http://lisa-home.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Provides:	lisa
Obsoletes:	kdenetwork-lisa
Obsoletes:	kdenetwork-lanbrowser
Requires(post,preun):/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LISa is a small daemon which is intended to run on end user systems.
It provides something like a "network neighbourhood", but only relying
on the TCP/IP protocol stack, no smb or whatever.

%description -l pl.UTF-8
LISA jest małym daemonem przeznaczonym do działania na komputerach
użytkowników. Dostarcza czegoś w rodzaju ,,Otoczenia Sieciowego'' ale
bazując jedynie na protokole TCP/IP a nie na SMB.

%package lslan
Summary:	Perl Script to print a LISa Host list on the command line
Summary(pl.UTF-8):	Skrypt w Perlu szukający otoczenia sieciowego z wiersza poleceń
Group:		Applications/Networking
Requires:	lisa

%description lslan
Lslan is a Perl Script to print a LISa Host list on the command line.
It it also configurable to test some standard server functions on the
hosts like SMB, FTP, HTTP ,VNC ,MySQL

%description lslan -l pl.UTF-8
Lslan to skrypt napisany w Perlu szukający w sieci hostów
udostępniających otoczenie sieciowe. Obok zasobów SMB możliwe jest
również wyszukiwanie kilku standardowych funkcji serwerów sieciowych
jak: FTP, HTTP ,VNC ,MySQL.

%prep
%setup -q -a 3
%patch -P1 -p1
%patch -P2 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sysconfdir}}

install lisarc $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/lisa
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lisa

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install lslan-0.2/lslan 	   $RPM_BUILD_ROOT%{_bindir}
install lslan-0.2/lslanrc.template $RPM_BUILD_ROOT%{_sysconfdir}/lslanrc

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
%doc README AUTHORS
%attr(755,root,root) %{_bindir}/lisa
%attr(755,root,root) %{_bindir}/reslisa
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lisarc
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/lisa
%attr(754,root,root) /etc/rc.d/init.d/lisa

%files lslan
%defattr(644,root,root,755)
%doc lslan-0.2/README lslan-0.2/lslanrc.template
%attr(755,root,root) %{_bindir}/lslan
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lslanrc
