#
# Conditional build:
%bcond_with	static_libs	# static library
#
Summary:	USRP client side C++ interface
Summary(pl.UTF-8):	Interfejs C++ strony klienckiej USRP
Name:		libusrp
Version:	3.4.5
Release:	2
License:	GPL v3+
Group:		Libraries
#Source0Download: https://github.com/osmocom/libusrp/releases
Source0:	https://github.com/osmocom/libusrp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a3b389b83712a9d7b47772674ac8e761
URL:		http://git.osmocom.org/libusrp/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	boost-devel >= 1.37
BuildRequires:	doxygen
BuildRequires:	guile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	sdcc >= 3.2.0
BuildRequires:	swig-python
BuildRequires:	xmlto
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
USRP client side C++ interface.

%description -l pl.UTF-8
Interfejs C++ strony klienckiej USRP.

%package devel
Summary:	Header files for USRP library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki USRP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= 1.37
Requires:	libstdc++-devel
Requires:	libusb-devel >= 1.0

%description devel
Header files for USRP library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki USRP.

%package static
Summary:	Static USRP library
Summary(pl.UTF-8):	Statyczna biblioteka USRP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static USRP library.

%description static -l pl.UTF-8
Statyczna biblioteka USRP.

%package apidocs
Summary:	API documentation for USRP library
Summary(pl.UTF-8):	Dokumentacja API biblioteki USRP
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description apidocs
API documentation for USRP library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki USRP.

%prep
%setup -q

echo '%{version}' > .tarball-version

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
# swig based --enable-guile and --enable-python are broken

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libusrp.la
# swig build is broken here, packaging is useless
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/gnuradio/swig
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/usrp-

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/usrp_cal_dc_offset
%attr(755,root,root) %{_bindir}/usrper
%attr(755,root,root) %{_libdir}/libusrp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libusrp.so.1
%{_datadir}/usrp

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libusrp.so
%{_includedir}/usrp
%{_pkgconfigdir}/usrp.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libusrp.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
