Name:		ming
Summary:	Ming - an SWF output library
Version:	0.0.9c
Release:	1
License:	LGPL
Group:		System Environment/Libraries
######		Unknown group!
URL:		http://www.opaque.net/ming/
Vendor:		Opaque Industries
Source0:	http://www.opaque.net/ming/%{name}-0_0_9c.tgz
Patch0:		%{name}-Makefile.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ming is a c library for generating SWF ("Flash") format movies, plus a
set of wrappers for using the library from c++ and popular scripting
languages like PHP, Python, and Ruby.

%prep
%setup -q
%patch -p1

%build
CFLAGS="%{rpmcflags}" \
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} PREFIX=$RPM_BUILD_ROOT%{_prefix} install

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libming.so*
%{_includedir}/ming.h

%doc CHANGES CREDITS LICENSE README
