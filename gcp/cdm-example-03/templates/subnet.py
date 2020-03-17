from templates import utils # pylint: disable=import-error

region = 'europe-west3'
ipCidrRange =  '10.2.0.0/16'
network = 'my-vpc'

def GenerateConfig(context):
    print('hi')
    resources = [{
        'name': context.env['name'],
        'type': 'compute.v1.subnetwork',
        'properties': {
            'region': region,
            'ipCidrRange': ipCidrRange,
            'network': utils.GetNetwork(context.env['project'], network)
        }
    }]
    return {'resources': resources}
