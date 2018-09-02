#
# Conditional build:
%bcond_without	php	# PHP binding
%bcond_with	java	# Java binding (native library build broken)
%bcond_with	ruby	# Ruby binding (unfinished)

%include	/usr/lib/rpm/macros.perl
Summary:	Ming - an SWF output library
Summary(pl.UTF-8):	Ming - biblioteka do produkcji plików SWF
Name:		ming
Version:	0.4.8
%define	ver_tag	%(echo %{version} | tr . _)
Release:	5
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/libming/libming/releases
Source0:	https://github.com/libming/libming/archive/%{name}-%{ver_tag}.tar.gz
# Source0-md5:	70c28c1e41d5888aa158e6e15644b742
Patch0:		%{name}-perl-shared.patch
Patch1:		am.patch
Patch3:		tcl-libx32.patch
URL:		http://www.libming.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2
BuildRequires:	giflib-devel >= 4.1
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	rpm-perlprov >= 4.0.2-24
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.344
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	swig
BuildRequires:	swig-tcl
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	zlib-devel
%if %{with php}
BuildRequires:	%{php_name}-cli
BuildRequires:	%{php_name}-devel >= 4:5.3
%endif
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

%package -n java-ming
Summary:	Ming Java classes
Summary(pl.UTF-8):	Klasy Ming dla Javy
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-ming
Ming Java classes.

%description -n java-ming -l pl.UTF-8
Klasy Ming dla Javy.

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

%package -n %{php_name}-ming
Summary:	Ming module for PHP
Summary(pl.UTF-8):	Moduł Ming dla PHP
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description -n %{php_name}-ming
PHP interface to Ming SWF generating library.

%description -n %{php_name}-ming -l pl.UTF-8
Interfejs PHP do biblioteki Ming generującej pliki SWF.

%package -n python-ming
Summary:	Ming Python module
Summary(pl.UTF-8):	Moduł biblioteki Ming dla języka Python
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs

%description -n python-ming
Ming Python module.

%description -n python-ming -l pl.UTF-8
Moduł biblioteki Ming dla języka Python.

%package -n tcl-ming
Summary:	Ming module for Tcl
Summary(pl.UTF-8):	Moduł Ming dla Tcl-a
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}
Requires:	tcl

%description -n tcl-ming
Tcl interface to Ming SWF generating library.

%description -n tcl-ming -l pl.UTF-8
Interfejs Tcl do biblioteki Ming generującej pliki SWF.

%prep
%setup -q -n libming-%{name}-%{ver_tag}
%patch0 -p1
%patch1 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-perl \
	%{?with_php:--enable-php} \
	--enable-python \
	--enable-tcl \
	--disable-silent-rules

%{__make} -j1 \
	mingc_ladir=%{_libdir}/tclming

%if %{with java}
%{__make} -C java_ext
CXXFLAGS="%{rpmcxxflags} %{rpmcppflags}" \
%{__make} -C java_ext/native \
	CXX="%{__cxx}" \
	LDFLAGS="%{rpmldflags} -L../../src/.libs -lming" \
	JAVADIR=%{_jvmdir}/java \
	NOVAR_SHLIBEXT=".so"
%endif

%if %{with ruby}
cd rb_ext
ln -sf ../src/.libs/libming.so .
ruby extconf.rb \
	--with-ming-include=../src \
        --with-ming-lib=../src/.libs
%{__make} \
	CC="%{__cc}" \
	optflags="%{rpmcflags}"
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	mingc_ladir=%{_libdir}/tclming

%if %{with php}
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/ming.ini
; Enable ming extension module
extension=ming.so
EOF
%endif

%if %{with java}
install -Dp java_ext/jswf.jar RPM_BUILD_ROOT%{_javadir}/jswf.jar
install java_ext/native/libjswf.so $RPM_BUILD_ROOT%{_libdir}
%endif

%if %{with ruby}
%{__make} -C rb_ext install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/SWF/.packlist
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/ming*.py
%{__rm} $RPM_BUILD_ROOT%{_libdir}/tclming/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
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

%if %{with java}
%files -n java-ming
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjswf.so
%{_javadir}/jswf.jar
%endif

%files -n perl-ming
%defattr(644,root,root,755)
%doc perl_ext/{README,TODO}
%{perl_vendorarch}/SWF.pm
%{perl_vendorarch}/SWF
%dir %{perl_vendorarch}/auto/SWF
%attr(755,root,root) %{perl_vendorarch}/auto/SWF/SWF.so
%{_mandir}/man3/SWF*.3pm*

%if %{with php}
%files -n %{php_name}-ming
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/ming.ini
%attr(755,root,root) %{php_extensiondir}/ming.so
%endif

%files -n python-ming
%defattr(644,root,root,755)
%doc py_ext/{README,TODO}
%attr(755,root,root) %{py_sitedir}/_mingc.so
%{py_sitedir}/ming*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitedir}/mingc-%{version}-py*.egg-info
%endif

%files -n tcl-ming
%defattr(644,root,root,755)
%doc tcl_ext/README
%dir %{_libdir}/tclming
%attr(755,root,root) %{_libdir}/tclming/mingc.so
