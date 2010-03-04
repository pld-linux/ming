%include	/usr/lib/rpm/macros.perl
Summary:	Ming - an SWF output library
Summary(pl.UTF-8):	Ming - biblioteka do produkcji plików SWF
Name:		ming
Version:	0.4.3
Release:	0.1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/ming/%{name}-%{version}.tar.gz
# Source0-md5:	9578ec38d973adabd9e8a534982da0b9
Patch0:		%{name}-build.patch
Patch1:		%{name}-perl-shared.patch
Patch2:		%{name}-libpng.patch
URL:		http://ming.sourceforge.net/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	giflib-devel
BuildRequires:	libpng-devel
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	rpm-perlprov >= 4.0.2-24
BuildRequires:	rpm-pythonprov
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
Summary:	Ming perl module
Summary(pl.UTF-8):	Moduł perla Ming
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ming-perl

%description -n perl-ming
Ming perl module - perl wrapper for Ming library.

%description -n perl-ming -l pl.UTF-8
Moduł perla Ming - perlowy wrapper do biblioteki Ming.

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure \
	--enable-perl \
	--enable-python

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/SWF/.packlist
rm $RPM_BUILD_ROOT%{py_sitedir}/ming*.py

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS README TODO
%attr(755,root,root) %{_libdir}/libming.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libming.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libming.so
%{_includedir}/ming.h
%{_includedir}/mingpp.h
%{_includedir}/ming_config.h

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
%attr(755,root,root) %{_bindir}/png2swf
%attr(755,root,root) %{_bindir}/raw2adpcm
%attr(755,root,root) %{_bindir}/swftoperl
%attr(755,root,root) %{_bindir}/swftophp
%attr(755,root,root) %{_bindir}/swftopython
%{_mandir}/man1/makeswf.1*

%files -n perl-ming
%defattr(644,root,root,755)
%doc perl_ext/{README,TODO}
%{perl_vendorarch}/SWF.pm
%{perl_vendorarch}/SWF
%dir %{perl_vendorarch}/auto/SWF
%{perl_vendorarch}/auto/SWF/SWF.bs
%attr(755,root,root) %{perl_vendorarch}/auto/SWF/SWF.so
%{_mandir}/man3/SWF*

%files -n python-ming
%defattr(644,root,root,755)
%doc py_ext/{README,TODO}
%attr(755,root,root) %{py_sitedir}/_mingc.so
%{py_sitedir}/ming*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitedir}/mingc-*.egg-info
%endif
