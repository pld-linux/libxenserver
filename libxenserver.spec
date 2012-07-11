Summary:	An SDK for Citrix XenServer, exposing the XenServer API
Summary(pl.UTF-8):	SDK dla Citrix XenServera, udostępniające API XenServer
Name:		libxenserver
Version:	6.0.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
# http://community.citrix.com/display/xs/Download+SDKs
Source0:	http://community.citrix.com/download/attachments/38633496/%{name}-%{version}-1-src.tar.bz2
# Source0-md5:	27faa9249092ad823cef3c3850240a21
Patch0:		%{name}-make.patch
URL:		http://community.citrix.com/display/xs/Home
BuildRequires:	curl-devel
BuildRequires:	libxml2-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libxenserver package contains a library of functions implementing
the Citrix XenServer API.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę funkcji implementujących API Citrix
XenServer.

%package devel
Summary:	Files needed for building applications with libxenserver
Summary(pl.UTF-8):	Pliki do tworzenia aplikacji z użyciem biblioteki libxenserver
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libxml2-devel

%description devel
The libxenserver-devel package contains header files necessary for
developing programs using the libxenserver Citrix XenServer API
library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów z
użyciem biblioteki libxenserver udostępniającej API Citrix XenServer.

%package static
Summary:	Static libxenserver library
Summary(pl.UTF-8):	Statyczna biblioteka libxenserver
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libxenserver library.

%description static -l pl.UTF-8
Statyczna biblioteka libxenserver.


%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__make} all libxenserver.a uberheader \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Iinclude $(xml2-config --cflags) $(curl-config --cflags) -W -Wall -std=c99 -fPIC" \
	LDFLAGS="%{rpmldflags}" \
	LIBS="$(xml2-config --libs) $(curl-config --libs)"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -p" \
	INSTALL_PROG="%{__install} -p -m755" \
	LIBDIR="%{_lib}"

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libxenserver.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenserver.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxenserver.so
# XXX: shared with xen-devel
%dir %{_includedir}/xen
%{_includedir}/xen/api

%files static
%defattr(644,root,root,755)
%{_libdir}/libxenserver.a
