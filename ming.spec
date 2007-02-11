%include	/usr/lib/rpm/macros.perl
Summary:	Ming - an SWF output library
Summary(pl):	Ming - biblioteka do produkcji plików SWF
Name:		ming
Version:	0.3.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/ming/%{name}-%{version}.tar.gz
# Source0-md5:	56b29eeb4fdd0b98c9ee62e25d14841d
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-build.patch
URL:		http://ming.sourceforge.net/
BuildRequires:	giflib-devel
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

%package static
Summary:	Ming static libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ming library

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
%configure
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS README TODO
%attr(755,root,root) %{_libdir}/libming.so.*

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
