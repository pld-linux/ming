
%include	/usr/lib/rpm/macros.perl
%include	/usr/lib/rpm/macros.python

Summary:	Ming - an SWF output library
Summary(pl):	Ming - biblioteka do produkcji plik�w SWF
Name:		ming
Version:	0.2a
Release:	5
License:	LGPL
Vendor:		Opaque Industries
Group:		Libraries
Source0:	http://www.opaque.net/ming/%{name}-%{version}.tgz
Patch0:		%{name}-dynamic-exts.patch
Patch1:		%{name}-soname.patch
Patch2:		%{name}-python.patch
URL:		http://www.opaque.net/ming/
BuildRequires:	python-devel
BuildRequires:	zlib-devel
BuildRequires:	rpm-perlprov >= 4.0.2-24
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		phpextdir	%(php-config --extension-dir)

%description
Ming is a C library for generating SWF ("Flash") format movies, plus a
set of wrappers for using the library from c++ and popular scripting
languages like PHP, Python, and Ruby.

%description -l pl
Ming jest bibliotek� w C do generowania animacji w formacie SWF
("Flash") wraz z zestawem wrapper�w do u�ywania jej z C++ i
popularnymi j�zykami skryptowymi, takimi jak PHP, Python i Ruby.

%package devel
Summary:	Ming development files
Summary(pl):	Pliki dla programist�w Ming
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for ming library (C and C++).

%description devel -l pl
Pliki nag��wkowe dla biblioteki ming (do C i C++).

%package -n perl-ming
Summary:	Ming perl module
Summary(pl):	Modu� perla Ming
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}
Obsoletes:	ming-perl

%description -n perl-ming
Ming perl module - perl wrapper for Ming library.

%description -n perl-ming -l pl
Modu� perla Ming - perlowy wrapper do biblioteki Ming.

%package -n python-ming
Summary:	Ming Python module
Summary(pl):	Modu� biblioteki Ming dla j�zyka Python
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}

%description -n python-ming
Ming Python module.

%description -n python-ming -l pl
Modu� biblioteki Ming dla j�zyka Python.

%package utils
Summary:	Ming utilities
Summary(pl):	Narz�dzia Ming
Group:		Applications/File

%description utils
Ming utilities:
- listswf - swf format disassembler
- listfdb - show contents of fdb font file
- makefdb - rip fdb font definition files out of a generator template
  file
- swftophp - attempt to make a php/ming script out of an swf file

%description utils -l pl
Narz�dzia Ming:
- listswf - disasembler plik�w swf
- listfdb - pokazuje zawarto�� plik�w font�w fdb
- makefdb - wyci�ga pliki definicji font�w fdb z pliku generatora
- swftophp - pr�buje zrobi� skrypt php/ming z pliku swf

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

mv -f rb_ext/README README.rb_ext

%build
%{__make} CC="%{__cc}" CFLAGS="%{rpmcflags}"

#%{__make} -C java_ext

(cd perl_ext
perl ./Makefile.PL
%{__make} OPTIMIZE="%{rpmcflags}"
)

%{__make} -C py_ext PYINCDIR=%{py_incdir}
#%{__make} -C rb_ext

(cd util
%{__make} CC="%{__cc} %{rpmcflags}" \
	listswf listaction swftophp makefdb
%{__cc} %{rpmcflags} -o listfdb listfdb.c
)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{py_sitedir}}

%{__make} PREFIX=$RPM_BUILD_ROOT%{_prefix} install

%{__make} -C perl_ext install DESTDIR=$RPM_BUILD_ROOT

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
%doc CHANGES CREDITS README TODO README.rb_ext
%attr(755,root,root) %{_libdir}/libming.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libming.so
%{_includedir}/ming.h
%{_includedir}/mingpp.h

%files -n perl-ming
%defattr(644,root,root,755)
%doc perl_ext/{README,TODO}
%{perl_sitearch}/SWF.pm
%{perl_sitearch}/SWF
%dir %{perl_sitearch}/auto/SWF
%{perl_sitearch}/auto/SWF/SWF.bs
%attr(755,root,root) %{perl_sitearch}/auto/SWF/SWF.so
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
