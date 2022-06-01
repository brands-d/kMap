from urllib import request
import json


#######################################################################
def get_molecule(ID,
              server='143.50.77.12', port='5002'):

    url = 'http://' + server + ':' + str(port)
    filename = 'ID%05i'%ID

    req = request.Request(url, headers={'Host': filename + '.hdfgroup.org'})
    with request.urlopen(req) as response:
        body = json.loads(response.read())

    uuid = body['root']

    fields = ['num_atom', 'chemical_numbers', 'atomic_coordinates']
    molecule = {}
    for field in fields:
        req = request.Request(url + '/groups/' + uuid + '/links/' + field, 
                          headers={'Host': filename + '.hdfgroup.org'})
        with request.urlopen(req) as response:
            body = json.loads(response.read())

        for href in body['hrefs']:
            if href['rel'] == 'target':
                uuid_field = href['href'].split('/')[-1]

        req = request.Request(url + '/datasets/' + uuid_field + '/value', 
                          headers={'Host': filename + '.hdfgroup.org'})

        with request.urlopen(req) as response:
            body = json.loads(response.read())  

        molecule[field] = body['value']

    return molecule

#####################################################################################################

def get_orbital(ID, orbital_number=0,
                server='143.50.77.12', port='5002'):

    url = 'http://' + server + ':' + str(port)
    filename = 'ID%05i'%ID

    req = request.Request(url + '/groups', headers={'Host': filename + '.hdfgroup.org'})
    with request.urlopen(req) as response:
        body = json.loads(response.read())


    group_uuid = body['groups'][orbital_number]

    psi = {}
    fields = ['x', 'y', 'z', 'data']
    for field in fields:
        req = request.Request(url + '/groups/' + group_uuid + '/links/'+field, 
                          headers={'Host': filename + '.hdfgroup.org'})
        with request.urlopen(req) as response:
            body = json.loads(response.read())

        for href in body['hrefs']:
            if href['rel'] == 'target':
                uuid = href['href'].split('/')[-1]

        req = request.Request(url + '/datasets/' + uuid + '/value', 
                          headers={'Host': filename + '.hdfgroup.org'})
      
        with request.urlopen(req) as response:
                body = json.loads(response.read())  

        psi[field] = body['value']

    psi['nx'] = len(psi['x'])
    psi['ny'] = len(psi['y'])
    psi['nz'] = len(psi['z'])
    psi['dx'] = psi['x'][1] - psi['x'][0]
    psi['dy'] = psi['y'][1] - psi['y'][0]
    psi['dz'] = psi['z'][1] - psi['y'][0]

    return psi

######### MAIN ###############################################################################
molecule = get_molecule(ID=2)
psi = get_orbital(ID=2, orbital_number=7)


