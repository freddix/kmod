%bcond_with	tests

Summary:	Linux kernel module handling
Name:		kmod
Version:	16
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
# Source0-md5:	3006a0287211212501cdfe1211b29f09
Source1:	%{name}-blacklist
Source2:	%{name}-usb
Source3:	%{name}-depmod-search.conf
Patch0:		%{name}-usr.patch
URL:		http://git.kernel.org/?p=utils/kernel/kmod/kmod.git;a=summary
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	module-init-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kmod is a set of tools to handle common tasks with Linux kernel
modules like insert, remove, list, check properties, resolve
dependencies and aliases.

These tools are designed on top of libkmod, a library that is shipped
with kmod. See libkmod/README for more details on this library and how
to use it. The aim is to be compatible with tools, configurations and
indexes from module-init-tools project.

%package libs
Summary:	Linux kernel module handling library
License:	LGPL v2.1+
Group:		Libraries

%description libs
libkmod was created to allow programs to easily insert, remove and
list modules, also checking its properties, dependencies and aliases.

%package devel
Summary:	Header files for %{name} library
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for %{name} library.

%prep
%setup -q

# upstream hardcodes /lib/modules as default path
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--with-xz		\
	--with-zlib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{{/etc/,%{_prefix}/lib}/{depmod,modprobe}.d,%{_sbindir}}

%{__make} install \
	pkgconfigdir=%{_pkgconfigdir} \
	DESTDIR=$RPM_BUILD_ROOT

# install symlinks
for prog in lsmod rmmod insmod modinfo modprobe depmod; do
	ln -s %{_bindir}/kmod $RPM_BUILD_ROOT%{_sbindir}/$prog
done

install %{SOURCE1} $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d/blacklist.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d/usb.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_prefix}/lib/depmod.d/search.conf

%check
%{?with_tests:%{__make} check}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README TODO

%dir /etc/depmod.d
%dir /etc/modprobe.d
%dir %{_prefix}/lib/depmod.d
%dir %{_prefix}/lib/modprobe.d
%{_prefix}/lib/modprobe.d/blacklist.conf
%{_prefix}/lib/modprobe.d/usb.conf
%{_prefix}/lib/depmod.d/search.conf

%attr(755,root,root) %{_bindir}/kmod
%attr(755,root,root) %{_sbindir}/lsmod
%attr(755,root,root) %{_sbindir}/rmmod
%attr(755,root,root) %{_sbindir}/insmod
%attr(755,root,root) %{_sbindir}/modinfo
%attr(755,root,root) %{_sbindir}/modprobe
%attr(755,root,root) %{_sbindir}/depmod

%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files libs
%defattr(644,root,root,755)
%doc libkmod/README
%attr(755,root,root) %ghost %{_libdir}/libkmod.so.?
%attr(755,root,root) %{_libdir}/libkmod.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkmod.so
%{_includedir}/libkmod.h
%{_pkgconfigdir}/libkmod.pc

