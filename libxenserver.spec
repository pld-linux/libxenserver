# TODO: C#(?), Java, Python
Summary:	An SDK for Citrix XenServer, exposing the XenServer API
Summary(pl.UTF-8):	SDK dla Citrix XenServera, udostępniające API XenServer
Name:		libxenserver
Version:	7.2.0
Release:	1
License:	BSD
Group:		Libraries
# download: http://xenserver.org/partners/developing-products-for-xenserver.html
# /Download SDK -> Software Development Kit
# e.g. https://www.citrix.com/downloads/xenserver/product-software/xenserver-72-standard-edition.html
# /SDK (then see at "rel" <a href=...> attribute)
Source0:	http://downloadns.citrix.com.edgesuite.net/12642/XenServer-%{version}-SDK.zip
# Source0-md5:	97b9f76d21dbddc055fb8a0af20e90e8
Patch0:		%{name}-make.patch
URL:		http://xenserver.org/partners/developing-products-for-xenserver.html
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

%package devel-internal
Summary:	Internal libxenserver header files
Summary(pl.UTF-8):	Wewnętrzne pliki nagłówkowe biblioteki libxenserver
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description devel-internal
Internal libxenserver header files.

%description devel-internal -l pl.UTF-8
Wewnętrzne pliki nagłówkowe biblioteki libxenserver.

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
%setup -q -n XenServer-SDK
%patch0 -p0

# precompiled binaries
%{__rm} libxenserver/bin/*

%build
%{__make} -C libxenserver/src all libxenserver.a \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Iinclude $(xml2-config --cflags) $(curl-config --cflags) -W -Wall -std=c99 -fPIC" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C libxenserver/src install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -p" \
	INSTALL_PROG="%{__install} -p -m755" \
	LIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc libxenserver/{COPYING,README}
%attr(755,root,root) %{_libdir}/libxenserver.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenserver.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxenserver.so
# XXX: shared with xen-devel
%dir %{_includedir}/xen
%{_includedir}/xen/api

%files devel-internal
%defattr(644,root,root,755)
%{_includedir}/xen*_internal.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libxenserver.a
