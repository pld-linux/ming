%include	/usr/lib/rpm/macros.perl
Summary:	Ming - an SWF output library
Summary(pl):	Ming - biblioteka do produkcji plików SWF
Name:		ming
Version:	0.2a
Release:	2
License:	LGPL
Vendor:		Opaque Industries
Group:		Libraries
Source0:	http://www.opaque.net/ming/%{name}-%{version}.tgz
Patch0:		%{name}-dynamic-exts.patch
Patch1:		%{name}-soname.patch
URL:		http://www.opaque.net/ming/
BuildRequires:	zlib-devel
BuildRequires:	rpm-perlprov >= 4.0.2-24
BuildRequires:	php-devel >= 4.0.6
#BuildRequires:	python-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		phpextdir	%(php-config --extension-dir)

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
Requires:	%{name} = %{version}

%description devel
Header files for ming library (C and C++).

%description devel -l pl
Pliki nag³ówkowe dla biblioteki ming (do C i C++).

%package -n perl-ming
Summary:	Ming perl module
Summary(pl):	Modu³ perla Ming
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}
Obsoletes:	ming-perl

%description -n perl-ming
Ming perl module - perl wrapper for Ming library.

%description -n perl-ming -l pl
Modu³ perla Ming - perlowy wrapper do biblioteki Ming.

%package php
Summary:	Ming PHP module
Summary(pl):	Modu³ PHP Ming
Group:		Libraries
Requires:	%{name} = %{version}

%description php
Ming PHP module.

%description php -l pl
Ming jako modu³ PHP.

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

%build
%{__make} CC="%{__cc}" CFLAGS="%{rpmcflags}"

#%{__make} -C java_ext

(cd perl_ext
perl ./Makefile.PL
%{__make} OPTIMIZE="%{rpmcflags}"
)

ln -sf ming-4.0.6.c php_ext/ming.c
%{__make} CC="%{__cc} %{rpmcflags}" -C php_ext

#%{__make} -C py_ext
#%{__make} -C rb_ext

(cd util
%{__make} CC="%{__cc} %{rpmcflags}" \
	listswf listaction swftophp makefdb
%{__cc} %{rpmcflags} -o listfdb listfdb.c
)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} PREFIX=$RPM_BUILD_ROOT%{_prefix} install

%{__make} -C perl_ext install DESTDIR=$RPM_BUILD_ROOT

(cd php_ext
install -d $RPM_BUILD_ROOT%{phpextdir}
install php_ming.so $RPM_BUILD_ROOT%{phpextdir}
)

install util/{listswf,listaction,listfdb,makefdb,swftophp} $RPM_BUILD_ROOT%{_bindir}

gzip -9nf CHANGES CREDITS README TODO \
	perl_ext/{README,TODO} \
	php_ext/README \
	py_ext/{README,TODO} \
	rb_ext/README \
	util/{README,TODO}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/libming.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libming.so
%{_includedir}/ming.h
%{_includedir}/mingpp.h

%files -n perl-ming
%defattr(644,root,root,755)
%doc perl_ext/*.gz
%{perl_sitearch}/SWF.pm
%{perl_sitearch}/SWF
%dir %{perl_sitearch}/auto/SWF
%{perl_sitearch}/auto/SWF/SWF.bs
%attr(755,root,root) %{perl_sitearch}/auto/SWF/SWF.so
%{_mandir}/man3/SWF*

%files php
%defattr(644,root,root,755)
%doc php_ext/*.gz
%attr(755,root,root) %{phpextdir}/*.so

%files utils
%defattr(644,root,root,755)
%doc util/*.gz
%attr(755,root,root) %{_bindir}/*
