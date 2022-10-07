%global         debug_package %{nil}
%global         __strip /bin/true
%global         _missing_build_ids_terminate_build 0

Name:           libnvjpeg2k
Version:        0.6.0.28
Release:        1%{?dist}
Summary:        NVIDIA JPEG 2K decoder (nvJPEG2000)
License:        NVIDIA EULA
URL:            https://developer.nvidia.com/nvjpeg
ExclusiveArch:  x86_64

# https://developer.nvidia.com/nvjpeg2000/downloads
Source0:        https://developer.download.nvidia.com/compute/libnvjpeg-2k/redist/libnvjpeg_2k/linux-x86_64/libnvjpeg_2k-linux-x86_64-%{version}-archive.tar.xz
Source1:        nvjpeg2k.pc

Obsoletes:      cuda-nvjpeg2k < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       cuda-nvjpeg2k = %{?epoch:%{epoch}:}%{version}-%{release}

Conflicts:      libnvjpeg2k0 < %{?epoch:%{epoch}:}%{version}-%{release}

%description
The nvJPEG2000 library accelerates the decoding of JPEG 2000 images on NVIDIA
GPUs. The library utilizes both CPU and GPU for decoding. Tier 2 decode stage
(First stage of decode, refer to the JPEG 2000 specification for details.) is
run on the CPU. All other stages of the decoding process are offloaded to the
GPU.

%package devel
Summary:        Development files for NVIDIA JPEG 2K decoder (nvJPEG2000)
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       cuda-devel%{_isa} >= 1:11
Conflicts:      libnvjpeg2k-devel < %{?epoch:%{epoch}:}%{version}

%description devel
This package provides development files for the NVIDIA JPEG 2K decoder (nvJPEG2000).

%package static
Summary:        Static libraries for NVIDIA JPEG 2K decoder (nvJPEG2000)
Requires:       pkgconf-pkg-config
Requires:       %{name}-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description static
This package contains static libraries for NVIDIA JPEG 2K decoder (nvJPEG2000).

%prep
%autosetup -n libnvjpeg_2k-linux-x86_64-%{version}-archive

%build
# Nothing to build

%install
mkdir -p %{buildroot}/%{_libdir}/pkgconfig/
mkdir -p %{buildroot}/%{_includedir}/cuda/

# Libraries
install -pm 755 lib/* %{buildroot}/%{_libdir}/

# Headers
install -pm 644 include/* %{buildroot}/%{_includedir}/cuda/

# pkg-config files
install -pm 644 %{SOURCE1} %{buildroot}/%{_libdir}/pkgconfig/

# Set proper variables
sed -i \
    -e 's|VERSION|%{version}|g' \
    -e 's|LIBDIR|%{_libdir}|g' \
    -e 's|INCLUDE_DIR|%{_includedir}/cuda|g' \
    %{buildroot}/%{_libdir}/pkgconfig/*.pc

%{?ldconfig_scriptlets}

%files
%license LICENSE
%{_libdir}/libnvjpeg2k.so.*

%files static
%{_libdir}/libnvjpeg2k_static.a

%files devel
%{_includedir}/cuda/nvjpeg2k.h
%{_includedir}/cuda/nvjpeg2k_version.h
%{_libdir}/libnvjpeg2k.so
%{_libdir}/pkgconfig/nvjpeg2k.pc

%changelog
* Fri Oct 07 2022 Simone Caronni <negativo17@gmail.com> - 0.6.0.28-1
- Update to 0.6.0.28.

* Thu Mar 31 2022 Simone Caronni <negativo17@gmail.com> - 0.5.0.25-1
- Update to 0.5.0.25.
- Rename to libnvjpeg2k.

* Tue Nov 02 2021 Simone Caronni <negativo17@gmail.com> - 0.4.0.24-1
- Update to 0.4.0.24.

* Wed Jul 21 2021 Simone Caronni <negativo17@gmail.com> - 0.3.0.23-1
- First build.