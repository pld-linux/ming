%include	/usr/lib/rpm/macros.perl
Summary:	Ming - an SWF output library
Summary(pl):	Ming - biblioteka do produkcji plików SWF
Name:		ming
Version:	0.2a
Release:	10
License:	LGPL
Vendor:		Opaque Industries
Group:		Libraries
Source0:	http://www.opaque.net/ming/%{name}-%{version}.tgz
# Source0-md5:	72b25da0af28d9cb025c2aaf3fd0185c
Patch0:		%{name}-dynamic-exts.patch
Patch1:		%{name}-soname.patch
Patch2:		%{name}-python.patch
Patch3:		%{name}-c++.patch
Patch4:		%{name}-types.patch
URL:		http://www.opaque.net/ming/
BuildRequires:	python-devel
BuildRequires:	rpm-perlprov >= 4.0.2-24
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ming is a C library for generating SWF ("Flash") format movies, plus a
set of wrappers for using the library from c++ and popular scripting
languages like PHP, Python, and Ruby.

%description -l pl
Ming jest bibliotek± w C do generowania animacji w formacie SWF
("Flash") wraz z zestawem wrapperów do u¿ywania jej z C++ i
popularnymi jêzykami skryptowymi, takimi jak PHP, Python i Ruby.

%package devel
Summary:	Ming development files
Summary(pl):	Pliki dla programistów Ming
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for ming library (C and C++).

%description devel -l pl
Pliki nag³ówkowe dla biblioteki ming (do C i C++).

%package -n perl-ming
Summary:	Ming perl module
Summary(pl):	Modu³ perla Ming
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ming-perl

%description -n perl-ming
Ming perl module - perl wrapper for Ming library.

%description -n perl-ming -l pl
Modu³ perla Ming - perlowy wrapper do biblioteki Ming.

%package -n python-ming
Summary:	Ming Python module
Summary(pl):	Modu³ biblioteki Ming dla jêzyka Python
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-ming
Ming Python module.

%description -n python-ming -l pl
Modu³ biblioteki Ming dla jêzyka Python.

%package utils
Summary:	Ming utilities
Summary(pl):	Narzêdzia Ming
Group:		Applications/File

%description utils
Ming utilities:
- listswf - swf format disassembler
- listfdb - show contents of fdb font file
- makefdb - rip fdb font definition files out of a generator template
  file
- swftophp - attempt to make a php/ming script out of an swf file

%description utils -l pl
Narzêdzia Ming:
- listswf - disasembler plików swf
- listfdb - pokazuje zawarto¶æ plików fontów fdb
- makefdb - wyci±ga pliki definicji fontów fdb z pliku generatora
- swftophp - próbuje zrobiæ skrypt php/ming z pliku swf

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__make} \
	CC="%{__cc}" \
	LIBDIR=%{_libdir} \
	CFLAGS="%{rpmcflags} -fPIC"

#%%{__make} -C java_ext

cd perl_ext
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	OPTIMIZE="%{rpmcflags}"
cd ..

%{__make} -C py_ext \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	PYINCDIR=%{py_incdir}

#%%{__make} -C rb_ext

cd util
%{__make} listswf listaction swftophp makefdb \
	CC="%{__cc} %{rpmcflags}"

%{__cc} %{rpmcflags} -o listfdb listfdb.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{py_sitedir}}

%{__make} install \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

%{__make} -C perl_ext install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C py_ext install \
	DESTDIR=$RPM_BUILD_ROOT \
	PYLIBDIR=$RPM_BUILD_ROOT%{py_libdir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

install util/{listswf,listaction,listfdb,makefdb,swftophp} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES CREDITS README TODO
%attr(755,root,root) %{_libdir}/libming.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libming.so
%{_includedir}/ming.h
%{_includedir}/mingpp.h

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
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py[co]

%files utils
%defattr(644,root,root,755)
%doc util/{README,TODO}
%attr(755,root,root) %{_bindir}/*
