def GenerateConfig(context):
    resources = [{
        'name': 'my_subnet',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'region': context.properties['region'],
            'ipCidrRange': context.properties['ipCidrRange'],
            'network': 'https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my_vpc'
        }
    }]
    return {'resources': resources}
