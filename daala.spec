#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Daala next-generation video codec
Summary(pl.UTF-8):	Daala - kodek obrazu następnej generacji
Name:		daala
Version:	0.0
%define	snap	20130928
Release:	0.%{snap}.1
License:	BSD
Group:		Libraries
# git clone https://git.xiph.org/daala.git
Source0:	%{name}.tar.xz
# Source0-md5:	b3ab1702b39a35bb564861a84863584f
URL:		http://xiph.org/daala/
BuildRequires:	SDL-devel
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.11
BuildRequires:	libogg-devel >= 1:1.3
BuildRequires:	libpng-devel
BuildRequires:	libtheora-devel
BuildRequires:	libtool >= 2:2
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	transfig
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Daala is the code-name for a new video compression technology. The
effort is a collaboration between Mozilla Foundation, Xiph.Org
Foundation and other contributors.

The goal of the project is to provide a free to implement, use and
distribute digital media format and reference implementation with
technical performance superior to H.265.

%description -l pl.UTF-8
Daala to nazwa kodowa nowej technologii kompresji obrazu. Próby te
są efektem współpracy Mozilla Foundation, Xiph.Org oraz innych
współpracowników.

Celem projektu jest dostarczenie wolnego w implementacji, użyciu i
rozpowszechnianiu formatu treści cyfrowej oraz wzorcowej implementacji
o wydajności lepszej niż H.265.

%package devel
Summary:	Header files for Daala libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Daala
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libogg-devel >= 1.3
Requires:	libpng-devel

%description devel
Header files for Daala libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Daala.

%package static
Summary:	Static Daala libraries
Summary(pl.UTF-8):	Statyczne biblioteki Daala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Daala libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Daala.

%package apidocs
Summary:	Daala API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek Daala
Group:		Documentation

%description apidocs
API documentation for Daala libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek Daala.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-doc} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdaala*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/daala

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_libdir}/libdaalabase.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdaalabase.so.0
%attr(755,root,root) %{_libdir}/libdaaladec.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdaaladec.so.0
%attr(755,root,root) %{_libdir}/libdaalaenc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdaalaenc.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdaalabase.so
%attr(755,root,root) %{_libdir}/libdaaladec.so
%attr(755,root,root) %{_libdir}/libdaalaenc.so
%{_includedir}/daala
%{_pkgconfigdir}/daaladec.pc
%{_pkgconfigdir}/daalaenc.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libdaalabase.a
%{_libdir}/libdaaladec.a
%{_libdir}/libdaalaenc.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
