Name:    ming
Summary: Ming - an SWF output library
Version: 0.0.9c
Release: 1
License: LGPL
Group:   System Environment/Libraries
URL:     http://www.opaque.net/ming/
Vendor:  Opaque Industries
Source:  http://www.opaque.net/ming/%{name}-0_0_9c.tgz
Patch:   ming-Makefile.patch
BuildRoot: /var/tmp/%{name}-%{version}-root

%description
Ming is a c library for generating SWF ("Flash") format movies, plus a set 
of wrappers for using the library from c++ and popular scripting languages 
like PHP, Python, and Ruby.

%prep
%setup -q
%patch -p1

%build
CFLAGS="$RPM_OPT_FLAGS" make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT%{_prefix} install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/libming.so*
%{_includedir}/ming.h

%doc CHANGES CREDITS LICENSE README

%changelog
* Mon Jan 29 2001 Troels Arvin <troels@arvin.dk>
  [0.0.9c-1.arvin]
- First Ming RPM package. Currently, the RPM doesn't include
  anyting but the shared library and the C-oriented include
  file. None of the wrappers for other languages are handled by this
  RPM, currently. Also, none of the utilities are included in the
  package yet.
