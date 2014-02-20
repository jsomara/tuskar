Name:	      openstack-tuskar
Version:	  0.0.8
Release:	  1%{?dist}
Summary:	  A service for managing OpenStack deployments

Group:		  Application/System
License:	  ASL 2.0
URL:		    https://github.com/openstack/tuskar
Source0:	  http://file.rdu.redhat.com/~jomara/tuskar/tuskar-%{version}.tar.gz

BuildArch:     noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-lockfile
BuildRequires: python-pbr
BuildRequires: python-sphinx >= 1.1.3

Requires: httpd
Requires: mod_wsgi
Requires: python-pbr
Requires: python-sqlalchemy
Requires: python-migrate
Requires: python-setuptools_git
Requires: python-amqplib
Requires: python-anyjson
Requires: python-argparse
Requires: python-eventlet
Requires: python-kombu
Requires: python-lxml
Requires: python-webob
Requires: python-greenlet
Requires: python-iso8601
Requires: python-flask
Requires: python-flask-babel
Requires: python-pecan
Requires: python-wsme
Requires: PyYAML
Requires: python-oslo-config
Requires: python-novaclient
Requires: python-keystoneclient
Requires: python-heatclient
Requires: openstack-tripleo-heat-templates

%description
Tuskar gives administrators the ability to control how and where OpenStack
services are deployed across the datacenter. Using Tuskar, administrators
divide hardware into "resource classes" that allow predictable elastic scaling
as cloud demands grow. This resource orchestration allows Tuskar users to
ensure SLAs, improve performance, and maximize utilization across the
datacenter.

%prep
%setup -q -n tuskar-%{version}

%build
export OSLO_PACKAGE_VERSION=1.2.0
%{__python} setup.py build

%install
export OSLO_PACKAGE_VERSION=1.2.0
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -m 0644 -D -p etc/tuskar-httpd.conf  %{buildroot}%{_sysconfdir}/httpd/conf.d/tuskar.conf

install -d -m 755 %{buildroot}%{_sharedstatedir}/tuskar
install -d -m 755 %{buildroot}%{_sysconfdir}/tuskar
install -d -m 755 %{buildroot}/srv/tuskar

install -m 0644 -D -p etc/tuskar.wsgi  %{buildroot}/srv/tuskar/tuskar.wsgi

# Move config to /etc
mv etc/tuskar/tuskar.conf.sample %{buildroot}%{_sysconfdir}/tuskar/tuskar.conf

%files
%doc LICENSE README.rst
%{python_sitelib}/tuskar
%{python_sitelib}/*.egg-info
# binaries for tuskar
%{_bindir}/tuskar-api
%{_bindir}/tuskar-dbsync
%{_bindir}/tuskar-manager
%dir /srv/tuskar
/srv/tuskar/tuskar.wsgi
%{_sharedstatedir}/tuskar
%dir %attr(0750, root, apache) %{_sysconfdir}/tuskar
%config(noreplace) %{_sysconfdir}/httpd/conf.d/tuskar.conf
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/tuskar/tuskar.conf

%changelog
* Wed Feb 19 2014 Jordan OMara <jomara@redhat.com> 0.7-1
- Adding PBR to buildrequires (jomara@redhat.com)

* Wed Feb 19 2014 Jordan OMara <jomara@redhat.com> 0.6-1
- Removing %%configure block (jomara@redhat.com)

* Wed Feb 19 2014 Jordan OMara <jomara@redhat.com> 0.5-1
- Fixing tuskar prep location (jomara@redhat.com)

* Wed Feb 19 2014 Jordan OMara <jomara@redhat.com> 0.4-1
- Minor fixes for httpd.conf location (jomara@redhat.com)

* Wed Feb 19 2014 Jordan OMara <jomara@redhat.com> 0.3-1
- Automatic commit of package [openstack-tuskar] release [0.2-1].
  (jomara@redhat.com)
- Initialized to use tito. (jomara@redhat.com)
- Initial commit of spec file, wsgi file and apache module for wsgi
  (jomara@redhat.com)
- Merge "Getting correct count and attributes from database"
  (jenkins@review.openstack.org)
- Merge "Fix tuskar docs building" (jenkins@review.openstack.org)
- Fix tuskar docs building (jason.dobies@redhat.com)
- Getting correct count and attributes from database (lsmola@redhat.com)

* Wed Feb 19 2014 Jordan OMara <jomara@redhat.com> 0.2-1
- new package built with tito

* Wed Feb 19 2014 Jordan OMara <jomara@redhat.com> - 0.0.1-1
- initial package
