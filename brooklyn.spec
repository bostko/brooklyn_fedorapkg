# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

%global basedir %{_var}/lib/%{name}
%global confdir %{_sysconfdir}/%{name}
%global homedir %{_datadir}/%{name}
%global libdir %{_javadir}/%{name}
%global logdir %{_var}/log/%{name}
%global packdname apache-brooklyn-%{version}-bin

%define _binaries_in_noarch_packages_terminate_build 0
%define __jar_repack 0
Name: brooklyn
Version: 0.10.0
Release: 0
Summary: Apache Brooklyn
License: ASL 2.0
Vendor: The Apache Software Foundation
URL: http://brooklyn.apache.org/
Group: Applications/Engineering
Packager: The Apache Software Foundation
Requires: java-headless >= 1:1.7.0
autoprov: yes
autoreq: yes
BuildArch: noarch

Source0: https://dist.apache.org/repos/dist/dev/brooklyn/apache-brooklyn-%{version}-rc2/apache-brooklyn-%{version}-rc2-bin.tar.gz
Source1: https://raw.githubusercontent.com/apache/brooklyn-dist/rel/apache-brooklyn-%{version}-rc2/shared-packaging/src/main/resources/conf/brooklyn.conf
Source2: https://raw.githubusercontent.com/apache/brooklyn-dist/rel/apache-brooklyn-%{version}-rc2/shared-packaging/src/main/resources/conf/logback.xml
Source3: %{name}.service
Source4: brooklyn-server
Source5: LICENSE

Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units

%description
Apache Brooklyn helps to model, deploy, and manage systems.
It supports blueprints in YAML or Java, and deploys them to many clouds and other target environments.
It monitors those deployments, maintains a live model, and runs autonomic policies to maintain their health.

%prep
%setup -q -n %{packdname}

%install
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{confdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{basedir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{libdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{logdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{homedir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}

%{__install} -m 0755 %{SOURCE4} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/server

%{__install} -m 0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{confdir}/brooklyn.conf
%{__install} -m 0644 %{SOURCE2} ${RPM_BUILD_ROOT}%{confdir}/logback.xml
%{__install} -m 0644 %{SOURCE3} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}.service

%{__cp} -a lib/brooklyn/*.jar ${RPM_BUILD_ROOT}%{libdir}

pushd ${RPM_BUILD_ROOT}%{homedir}
    %{__ln_s} %{libdir} lib
    %{__ln_s} %{confdir} conf
    %{__ln_s} %{logdir} logs
popd

%files
%defattr(0644,root,brooklyn,755)
%config %dir %attr(755,brooklyn,brooklyn)  "%{basedir}"
%config %dir %attr(755,brooklyn,brooklyn) "%{_javadir}/%{name}"
%config %dir %attr(755,brooklyn,brooklyn) "%{libdir}"
%config %dir %attr(700,brooklyn,brooklyn) "%{logdir}"
%config %attr(600,brooklyn,brooklyn)  "%{confdir}/brooklyn.conf"
%config %attr(644,brooklyn,brooklyn)  "%{confdir}/logback.xml"
%config %attr(644,brooklyn,brooklyn)  "%{libdir}/*.jar"
%attr(0644,root,root) %{_unitdir}/%{name}.service
%attr(0755,root,root) %{_libexecdir}/%{name}/server

%dir %{homedir}
%{homedir}/lib
%{homedir}/conf
%{homedir}/logs

%pre
/bin/getent group brooklyn || /sbin/groupadd -r brooklyn
/bin/getent passwd brooklyn || /sbin/useradd -r -g brooklyn -d %{basedir} -s /usr/share/nologin brooklyn

%post
%systemd_post brooklyn.service

%preun
%systemd_preun brooklyn.service

%postun
%systemd_postun brooklyn.service

%changelog
* Wed Dec 7 2016 Valentin Aitken <bostko@gmail.com>
- Apache Broklyn 0.10.0.rc1

* Fri Apr 15 2016 Valentin Aitken <bostko@gmail.com>
- Apache Broklyn 0.9.0
