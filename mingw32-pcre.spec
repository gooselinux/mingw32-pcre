%global __strip %{_mingw32_strip}
%global __objdump %{_mingw32_objdump}

%global _use_internal_dependency_generator 0
%global __find_requires %{_mingw32_findrequires}
%global __find_provides %{_mingw32_findprovides}

%define __debug_install_post %{_mingw32_debug_install_post}

Name:		mingw32-pcre
Version:	8.10
Release:	2%{?dist}.4
Summary:	MinGW Windows pcre library

Group:		Development/Libraries

License:	BSD
URL:		http://www.pcre.org/
Source0:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%{version}.tar.gz
Patch0:		pcre-8.10-multilib.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Requires:	pkgconfig

BuildRequires:	redhat-rpm-config
BuildRequires:	mingw32-filesystem >= 56
BuildRequires:	mingw32-gcc
BuildRequires:	mingw32-gcc-c++
BuildRequires:	mingw32-binutils

# New libtool to get rid of rpath
BuildRequires: autoconf, automake, libtool

%{?_mingw32_debug_package}

%description
Cross compiled Perl-compatible regular expression library for use with mingw32.

PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%prep
%setup -q -n pcre-%{version}

# Get rid of rpath
%patch0 -p1 -b .multilib
libtoolize --copy --force && autoreconf
# One contributor's name is non-UTF-8
for F in ChangeLog; do
    iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
    touch --reference "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done

%build
%{_mingw32_configure} --enable-utf8 --enable-unicode-properties --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/doc/*
rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/man/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_mingw32_bindir}/pcre-config
%{_mingw32_bindir}/pcregrep.exe
%{_mingw32_bindir}/pcretest.exe
%{_mingw32_bindir}/libpcre*.dll
%{_mingw32_libdir}/libpcre*.dll.a
%{_mingw32_libdir}/libpcre*.la
%{_mingw32_libdir}/pkgconfig/libpcre*.pc
%{_mingw32_includedir}/*.h

%doc AUTHORS COPYING LICENCE NEWS README ChangeLog

%changelog
* Mon Dec 27 2010 Andrew Beekhof <abeekhof@redhat.com> - 8.10-2.4
- Rebuild everything with gcc-4.4
  Related: rhbz#658833

* Fri Dec 24 2010 Andrew Beekhof <abeekhof@redhat.com> - 8.10-2.3
- The use of ExclusiveArch conflicts with noarch, using an alternate COLLECTION to limit builds
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 8.10-2.2
- Only build mingw packages on x86_64
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 8.10-2.1
- Bump the revision to avoid tag collision
  Related: rhbz#658833

* Mon Sep 20 2010 Adam Stokes <astokes@redhat.com> - 8.10-2
- Restore changes from the native package to pass package review process

* Wed Jul 21 2010 Ryan O'Hara <rohara@redhat.com> - 8.10-1
- Initial spec file.
