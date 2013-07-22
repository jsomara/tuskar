# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Red Hat                # All Rights Reserved.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

#
from novaclient.v1_1 import client
from oslo.config import cfg
import simpleyaml
from tuskar.common import exception
from tuskar.openstack.common import jsonutils
from tuskar.openstack.common import log

nova_opts = [
    cfg.StrOpt('nova_overcloud_config',
               default='etc/tuskar/nova_overcloud_config.yml',
               help='nova overcloud keystone uri and credentials'),
    ]

LOG = log.getLogger(__name__)
CONF = cfg.CONF
CONF.register_opts(nova_opts)

class NovaClient(object):

    def __init__(self):
        #grab client params from nova_overcloud_config.yml:
        try:
            config_file = open(CONF.nova_overcloud_config)
            client_params = simpleyaml.safe_load(config_file)
            config_file.close()
        except Exception:
            raise
        self.nova_client = client.Client(client_params['nova_username'], client_params['nova_password'],
            client_params['nova_tenantname'], client_params['keystone_url'] , service_type="compute")

    def get_flavors(self):
        """Calls out to Nova for a list of detailed flavor information."""
        try:
            flavors = self.nova_client.flavors.list()
        except Exception:
            raise
        #should convert response to some local Flavor object - controller/db?
        #TODO ^^^ FIXME - right now we aren't using this method
        return flavors

    #returns newly created flavor uuid from nova
    def create_flavor(self, flavor_data, rc_name):
        try:
            ram, cpu, disk = self.__extract_from_capacities(flavor_data)
            name = "%s.%s" %(rc_name, flavor_data.name)
            nova_flavor = self.nova_client.flavors.create(name, ram, cpu, disk)
            return nova_flavor.id
        except Exception:
            raise
        return nova_flavor

    def delete_flavor(self, nova_flavor_id):
        try:
            self.nova_client.flavors.delete(nova_flavor_id)
        except Exception:
            raise
        return True

    def __extract_from_capacities(self, flavor_data):
        ram = cpu = disk = ""
        for c in flavor_data.capacities:
            if c.name == "memory":
                ram = c.value
            elif c.name == "cpu":
                cpu = c.value
            elif c.name == "storage":
                disk = c.value
        return ram, cpu, disk

