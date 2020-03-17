from templates import utils # pylint: disable=import-error

region = 'europe-west3'
ipCidrRange =  '10.2.0.0/16'

def GenerateConfig(context):
    network = context.env['name']

    resources = [{
        'name': network,
        'type': 'compute.v1.subnetwork',
        'properties': {
            'region': region,
            'ipCidrRange': ipCidrRange,
            'network': utils.GetNetwork(context.env['project'], network)
        }
    }]
    return {'resources': resources}
