%include	/usr/lib/rpm/macros.perl
Summary:	Ming - an SWF output library
Summary(pl):	Ming - biblioteka do produkcji plikÛw SWF
Name:		ming
Version:	0.2a
Release:	1
License:	LGPL
Vendor:		Opaque Industries
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	‚…¬Ã…œ‘≈À…
Group(uk):	‚¶¬Ã¶œ‘≈À…
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
("Flash") wraz z zestawem wrapperÛw do uøywania jej z C++ i
popularnymi jÍzykami skryptowymi, takimi jak PHP, Python i Ruby.

%package devel
Summary:	Ming development files
Summary(pl):	Pliki dla programistÛw Ming
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name} = %{version}

%description devel
Header files for ming library (C and C++).

%description devel -l pl
Pliki nag≥Ûwkowe dla biblioteki ming (do C i C++).

%package -n perl-ming
Summary:	Ming perl module
Summary(pl):	Modu≥ perla Ming
Group:		Development/Languages/Perl
Group(de):	Entwicklung/Sprachen/Perl
Group(pl):	Programowanie/JÍzyki/Perl
Requires:	%{name} = %{version}
Obsoletes:	ming-perl

%description perl
Ming perl module - perl wrapper for Ming library.

%description perl -l pl
Modu≥ perla Ming - perlowy wrapper do biblioteki Ming.

%package php
Summary:	Ming PHP module
Summary(pl):	Modu≥ PHP Ming
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	‚…¬Ã…œ‘≈À…
Group(uk):	‚¶¬Ã¶œ‘≈À…
Requires:	%{name} = %{version}

%description php
Ming PHP module.

%description php -l pl
Ming jako modu≥ PHP.

%package utils
Summary:	Ming utilities
Summary(pl):	NarzÍdzia Ming
Group:		Applications/File
Group(de):	Applikationen/Datei
Group(pl):	Aplikacje/Pliki

%description utils
Ming utilities:
- listswf - swf format disassembler
- listfdb - show contents of fdb font file
- makefdb - rip fdb font definition files out of a generator template
  file
- swftophp - attempt to make a php/ming script out of an swf file

%description utils -l pl
NarzÍdzia Ming:
- listswf - disasembler plikÛw swf
- listfdb - pokazuje zawarto∂Ê plikÛw fontÛw fdb
- makefdb - wyci±ga pliki definicji fontÛw fdb z pliku generatora
- swftophp - prÛbuje zrobiÊ skrypt php/ming z pliku swf

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
