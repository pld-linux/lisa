Summary:	-
Summary(pl):	-
Name:		lisa
Version:	0.2.1
Release:	0.1
License:	- (enter GPL/LGPL/BSD/BSD-like/other license name here)
Group:		-
Source0:	http://lisa-home.sourceforge.net/src/lisa-0.2.1.tar.bz2
URL:		http://lisa-home.sourceforge.net/
#BuildRequires:	-
#PreReq:		-
#Requires:	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

%prep
%setup -q
#%setup -q -n %{name}-%{version}.orig -a 1
#%patch0 -p1

%build
#aclocal
#%{__autoconf}
#autoheader
#%{__automake}
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%preun

%post

%postun

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
