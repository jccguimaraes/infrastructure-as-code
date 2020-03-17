API_URL = 'https://www.googleapis.com/compute/v1/projects/'

def GetNetwork(projectId, network):
    return API_URL + projectId + '/global/networks/' + network