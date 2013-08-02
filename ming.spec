%include	/usr/lib/rpm/macros.perl
Summary:	Ming - an SWF output library
Summary(pl.UTF-8):	Ming - biblioteka do produkcji plików SWF
Name:		ming
Version:	0.4.5
Release:	2
License:	LGPL
Group:		Libraries
Source0:	http://downloads.sourceforge.net/ming/%{name}-%{version}.tar.gz
# Source0-md5:	a35735a1c4f51681b96bcbfba58db2a0
Patch0:		%{name}-perl-shared.patch
Patch1:		am.patch
URL:		http://ming.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	freetype-devel
BuildRequires:	giflib-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	php-devel >= 4:5.3
BuildRequires:	php-program
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	rpm-perlprov >= 4.0.2-24
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	swig
BuildRequires:	swig-tcl
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ming is a C library for generating SWF ("Flash") format movies, plus a
set of wrappers for using the library from c++ and popular scripting
languages like PHP, Python, and Ruby.

%description -l pl.UTF-8
Ming jest biblioteką w C do generowania animacji w formacie SWF
("Flash") wraz z zestawem wrapperów do używania jej z C++ i
popularnymi językami skryptowymi, takimi jak PHP, Python i Ruby.

%package devel
Summary:	Ming development files
Summary(pl.UTF-8):	Pliki dla programistów Ming
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	giflib-devel

%description devel
Header files for ming library (C and C++).

%description devel -l pl.UTF-8
Pliki nagłówkowe dla biblioteki ming (do C i C++).

%package static
Summary:	Ming static library
Summary(pl.UTF-8):	Statyczna biblioteka Ming
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Ming library.

%description static -l pl.UTF-8
Statyczna biblioteka Ming.

%package utils
Summary:	Ming utilities
Summary(pl.UTF-8):	Narzędzia Ming
Group:		Applications/File

%description utils
Ming utilities:
- listswf - swf format disassembler
- listfdb - show contents of fdb font file
- makefdb - rip fdb font definition files out of a generator template
  file
- swftophp - attempt to make a php/ming script out of an swf file

%description utils -l pl.UTF-8
Narzędzia Ming:
- listswf - disasembler plików swf
- listfdb - pokazuje zawartość plików fontów fdb
- makefdb - wyciąga pliki definicji fontów fdb z pliku generatora
- swftophp - próbuje zrobić skrypt php/ming z pliku swf

%package -n perl-ming
Summary:	Ming Perl module
Summary(pl.UTF-8):	Moduł Perla Ming
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ming-perl

%description -n perl-ming
Ming perl module - perl wrapper for Ming library.

%description -n perl-ming -l pl.UTF-8
Moduł perla Ming - perlowy wrapper do biblioteki Ming.

%package -n php-ming
Summary:	Ming module for PHP
Summary(pl.UTF-8):	Moduł Ming dla PHP
Group:		Development/Langauges/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description -n php-ming
PHP interface to Ming SWF generating library.

%description -n php-ming -l pl.UTF-8
Interfejs PHP do biblioteki Ming generującej pliki SWF.

%package -n python-ming
Summary:	Ming Python module
Summary(pl.UTF-8):	Moduł biblioteki Ming dla języka Python
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-ming
Ming Python module.

%description -n python-ming -l pl.UTF-8
Moduł biblioteki Ming dla języka Python.

%package -n tcl-ming
Summary:	Ming module for Tcl
Summary(pl.UTF-8):	Moduł Ming dla Tcl-a
Group:		Development/Langauges/Tcl
Requires:	%{name} = %{version}-%{release}
Requires:	tcl

%description -n tcl-ming
Tcl interface to Ming SWF generating library.

%description -n tcl-ming -l pl.UTF-8
Interfejs Tcl do biblioteki Ming generującej pliki SWF.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__automake}
%configure \
	--enable-perl \
	--enable-php \
	--enable-python \
	--enable-tcl

%{__make} -j1 \
	mingc_ladir=%{_libdir}/tclming

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	mingc_ladir=%{_libdir}/tclming

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/ming.ini
; Enable ming extension module
extension=ming.so
EOF

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/SWF/.packlist
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/ming*.py
%{__rm} $RPM_BUILD_ROOT%{_libdir}/tclming/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_libdir}/libming.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libming.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libming.so
%{_libdir}/libming.la
%{_includedir}/ming.h
%{_includedir}/mingpp.h
%{_pkgconfigdir}/libming.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libming.a

%files utils
%defattr(644,root,root,755)
%doc util/{README,TODO}
%attr(755,root,root) %{_bindir}/dbl2png
%attr(755,root,root) %{_bindir}/gif2dbl
%attr(755,root,root) %{_bindir}/gif2mask
%attr(755,root,root) %{_bindir}/listaction
%attr(755,root,root) %{_bindir}/listaction_d
%attr(755,root,root) %{_bindir}/listfdb
%attr(755,root,root) %{_bindir}/listjpeg
%attr(755,root,root) %{_bindir}/listmp3
%attr(755,root,root) %{_bindir}/listswf
%attr(755,root,root) %{_bindir}/listswf_d
%attr(755,root,root) %{_bindir}/makefdb
%attr(755,root,root) %{_bindir}/makeswf
%attr(755,root,root) %{_bindir}/ming-config
%attr(755,root,root) %{_bindir}/png2dbl
%attr(755,root,root) %{_bindir}/raw2adpcm
%attr(755,root,root) %{_bindir}/swftocxx
%attr(755,root,root) %{_bindir}/swftoperl
%attr(755,root,root) %{_bindir}/swftophp
%attr(755,root,root) %{_bindir}/swftopython
%attr(755,root,root) %{_bindir}/swftotcl

%files -n perl-ming
%defattr(644,root,root,755)
%doc perl_ext/{README,TODO}
%{perl_vendorarch}/SWF.pm
%{perl_vendorarch}/SWF
%dir %{perl_vendorarch}/auto/SWF
%{perl_vendorarch}/auto/SWF/SWF.bs
%attr(755,root,root) %{perl_vendorarch}/auto/SWF/SWF.so
%{_mandir}/man3/SWF*

%files -n php-ming
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/ming.ini
%attr(755,root,root) %{php_extensiondir}/ming.so

%files -n python-ming
%defattr(644,root,root,755)
%doc py_ext/{README,TODO}
%attr(755,root,root) %{py_sitedir}/_mingc.so
%{py_sitedir}/ming*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitedir}/mingc-*.egg-info
%endif

%files -n tcl-ming
%defattr(644,root,root,755)
%doc tcl_ext/README
%dir %{_libdir}/tclming
%attr(755,root,root) %{_libdir}/tclming/mingc.so
