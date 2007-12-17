%define	major 0
%define libname %mklibname avlmap %{major}
%define develname %mklibname avlmap -d

Summary:	AVLMAP - Binary tree and mapping library
Name:		avlmap
Version:	0.12.2
Release:	%mkrel 5
Group:		System/Libraries
License:	LGPL
URL:		http://avlmap.slashusr.org/
Source0:	http://avlmap.slashusr.org/download/avlmap-%{version}.tar.bz2
Provides:	libavlmap

%description
The avlmap library implements a data mapping abstraction in
function calls, along with an underlying AVL balanced binary
search tree implementation. 

%package -n	%{libname}
Summary:	AVLMAP - Binary tree and mapping library
Group:          System/Libraries

%description -n	%{libname}
The avlmap library implements a data mapping abstraction in
function calls, along with an underlying AVL balanced binary
search tree implementation. 

%package -n	%{develname}
Summary:	Development library and header files for the %{name} library
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname avlmap 0 -d}

%description -n %{develname}
The avlmap library implements a data mapping abstraction in
function calls, along with an underlying AVL balanced binary
search tree implementation. 

%package -n	%{name}-utils
Summary:	Various utilities using the %{libname} library
Group:          Text tools

%description -n	%{name}-utils
Various utilities using the %{libname} library

* wordstat - Count the frequency of different word items in the
             input.

* wordstat - Count the frequency of different word items in the
             input.

* wordscan - like wordstat but don't actually do anything with
             mappings.

%prep

%setup -q -n %{name}-%{version}

%build

#echo "%{optflags} -fPIC" > Compile.opt
sh ./configure --prefix=%{_prefix}

# really whacked configure thing...
WARN="-Werror -Wall -Wno-cast-qual -Wwrite-strings -Wnested-externs -Winline -Wuninitialized"
OPT="%{optflags} -fomit-frame-pointer -funsigned-char -funsigned-bitfields -frerun-loop-opt -finline -finline-functions"

perl -pi -e "s|^lib_warn = .*|lib_warn = $WARN|g" build/Makefile
perl -pi -e "s|^pgm_warn = .*|pgm_warn = $WARN|g" build/Makefile
perl -pi -e "s|^lib_feat = .*|lib_feat = $OPT|g" build/Makefile
perl -pi -e "s|^pgm_feat = .*|pgm_feat = $OPT|g" build/Makefile

make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_includedir}/avlmap
install -d %{buildroot}%{_libdir}

# install binaries
install -m0755 build/bin/itemfreq %{buildroot}%{_bindir}/
install -m0755 build/bin/wordcount %{buildroot}%{_bindir}/
install -m0755 build/bin/wordcounts %{buildroot}%{_bindir}/
install -m0755 build/bin/wordfreq %{buildroot}%{_bindir}/

# install headers
install -m0644 build/include/avlmap/*.h %{buildroot}%{_includedir}/avlmap/

# install the shared lib
install -m0755 build/lib/libavlmap.so.%{version} %{buildroot}%{_libdir}/
ln -snf libavlmap.so.%{version} %{buildroot}%{_libdir}/libavlmap.so.0.12
ln -snf libavlmap.so.%{version} %{buildroot}%{_libdir}/libavlmap.so.0
ln -snf libavlmap.so.%{version} %{buildroot}%{_libdir}/libavlmap.so

# install the static lib
install -m0755 build/lib/libavlmap.a.%{version} %{buildroot}%{_libdir}/libavlmap.a

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc ChangeLog README
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc map/doc/*
%attr(0755,root,root) %{_libdir}/lib*.so
%attr(0644,root,root) %{_libdir}/lib*.a
%attr(0644,root,root) %{_includedir}/avlmap/*.h

%files -n %{name}-utils
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
