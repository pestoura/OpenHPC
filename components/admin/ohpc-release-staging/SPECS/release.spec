#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%global ohpc_bootstrap 1
%include %{_sourcedir}/OHPC_macros

%if 0%{?rhel}
%define disttag .el8
%endif

%if 0%{?suse_version}
%define disttag .leap15
%endif


Summary:  OpenHPC release files
Name:     ohpc-release-staging
Version:  %{ohpc_version}
Release:  1%{?disttag}
License:  Apache-2.0
Group:    %{PROJ_NAME}/admin
URL:      https://github.com/openhpc/ohpc
Source1:  RPM-GPG-KEY-OpenHPC-2

Provides: ohpc-release = %{version}

%if 0%{?rhel}
Requires: epel-release
Requires: redhat-release >= 8.1
%endif
%if 0%{?suse_version}
Requires: (suse-release >= 15.1 or sles-release >= 15.1)
%endif

%description

Collection of OpenHPC release files including package repository
definition. The factory release is intended for pre-release testing
from the staging repo area.

%prep

%build

%install

%{__mkdir} ${RPM_BUILD_ROOT}/etc

# /etc/ohpc-release

cat >> ${RPM_BUILD_ROOT}/etc/ohpc-release <<EOF
OpenHPC release %{version} (%{_repository})
HOME_URL="http://openhpc.community"
BUG_REPORT_URL="https://github.com/openhpc/ohpc/issues"
EOF

# package repository definitions

%if 0%{?suse_version}
%define __repodir /etc/zypp/repos.d
%else
%define __repodir /etc/yum.repos.d
%endif

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{__repodir}

# additional logic to determine whether this is a micro update release or
# not. If not, then we enable factory for the initial minor release. If it is a
# micro update, we enable factory for the update instead.

cat >> ${RPM_BUILD_ROOT}/%{__repodir}/OpenHPC.repo <<EOF
[OpenHPC]
name=OpenHPC-%{ohpc_version} - Base
baseurl=%{ohpc_repo}/OpenHPC/%{ohpc_version}/%{_repository}
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenHPC-2

[OpenHPC-updates]
name=OpenHPC-%{ohpc_version} - Updates
baseurl=%{ohpc_repo}/.staging/OpenHPC/%{ohpc_version}/update.2.1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenHPC-2
enabled=1
EOF


# repository GPG key

install -D -m 0644 %SOURCE1 ${RPM_BUILD_ROOT}/etc/pki/rpm-gpg/RPM-GPG-KEY-OpenHPC-2

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%config /etc/ohpc-release

%if 0%{?suse_version}
%dir /etc/zypp
%endif

%{__repodir}
/etc/pki
