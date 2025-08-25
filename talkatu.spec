#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Talkatu - GTK4 widgets for chat applications library
Summary(pl.UTF-8):	Talkatu - biblioteka widżetów GTK4 dla komunikatorów
Name:		talkatu
Version:	0.2.0
Release:	4
License:	GPL v2+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/pidgin/%{name}-%{version}.tar.xz
# Source0-md5:	abf74f6f5c50c8b6c1daafce3e56117d
URL:		https://keep.imfreedom.org/talkatu/talkatu/
BuildRequires:	cmark-devel >= 0.28.0
# -std=c17
BuildRequires:	gcc >= 6:7
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.52.0
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk4-devel >= 4.6.0
BuildRequires:	gumbo-parser-devel >= 0.10
BuildRequires:	help2man
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
Requires:	cmark-lib >= 0.28.0
Requires:	glib2 >= 1:2.52.0
Requires:	gtk4 >= 4.6.0
Requires:	gumbo-parser >= 0.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Talkatu is a collection of GTK4 widgets that are useful for chat
applications.

%description -l pl.UTF-8
Talkatu to zbiór widżetów GTK4 przydatnych dla komunikatorów.

%package devel
Summary:	Header files for Talkatu library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Talkatu
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cmark-devel >= 0.28.0
Requires:	glib2-devel >= 1:2.52.0
Requires:	gtk4-devel >= 4.6.0
Requires:	gumbo-parser-devel >= 0.10

%description devel
Header files for Talkatu library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Talkatu.

%package static
Summary:	Static Talkatu library
Summary(pl.UTF-8):	Statyczna biblioteka Talkatu
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Talkatu library.

%description static -l pl.UTF-8
Statyczna biblioteka Talkatu.

%package -n vala-talkatu
Summary:	Vala API for Talkatu library
Summary(pl.UTF-8):	API języka Vala do biblioteki Talkatu
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-talkatu
Vala API for Talkatu library.

%description -n vala-talkatu -l pl.UTF-8
API języka Vala do biblioteki Talkatu.

%package apidocs
Summary:	API documentation for Talkatu library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Talkatu
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Talkatu library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Talkatu.

%prep
%setup -q

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_apidocs:-Ddoc=false}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/talkatu $RPM_BUILD_ROOT%{_gidocdir}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) %{_bindir}/talkatu-demo
%attr(755,root,root) %{_libdir}/libtalkatu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtalkatu.so.0
%{_libdir}/girepository-1.0/Talkatu-0.0.typelib
%{_mandir}/man1/talkatu-demo.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtalkatu.so
%{_includedir}/talkatu-1.0
%{_datadir}/gir-1.0/Talkatu-0.0.gir
%{_pkgconfigdir}/talkatu.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtalkatu.a
%endif

%files -n vala-talkatu
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/talkatu.deps
%{_datadir}/vala/vapi/talkatu.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/talkatu
%endif
