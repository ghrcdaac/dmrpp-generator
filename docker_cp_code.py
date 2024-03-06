
def wait_on_container():
    # Wait for container to be running
    logger.info('Waiting on dmrpp-generator container...')
    while True:
        complete = subprocess.run(
            ['docker', 'ps', '--format', '"{{.ID}}"', '-f', 'name=dmrpp-generator',
             '-f' 'status=running'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        out = complete.stdout.decode()
        # logger.info(out)
        if out:
            #  Get the container ID
            container_id = out.replace('"', '').strip()
            logger.info(f'Container running {container_id}')
            break
        time.sleep(1)

    return container_id


def create_manifest(nc_hdf_path):
    # manifest = tempfile.mkstemp(prefix='manifest-', suffix='.in', dir=tempfile.gettempdir(), text=True)
    manifest_path = f'{nc_hdf_path}/manifest.in'
    logger.info(f'Creating manifest: {manifest_path}')
    file_list = os.listdir(nc_hdf_path)
    file_list.sort()
    logger.info('Adding files: ')
    with open(manifest_path, 'w+') as manifest:
        for file in file_list:
            file_path = f'{nc_hdf_path}/{file}'
            logger.info(f' {file_path}')
            manifest.write(f'{file} {str(os.stat(file_path).st_size)}\n')
    return manifest_path

def wait_on_manifest():
    manifest_in = '/home/worker/inputs/manifest.in'
    while not os.path.isfile(manifest_in):
        logger.info('Waiting on manifest file...')
        time.sleep(1)

    # Read file list
    input_files = {}
    with open(manifest_in, 'r') as manifest:
        for line in manifest.readlines():
            logger.info(f'manifest: {line}')
            split_val = line.strip().split(' ')
            input_files.update({split_val[0]: int(split_val[1])})
    # os.remove(manifest_in)

    logger.info(f'input_files: {input_files}')

    # Wait on copying operations to be complete
    logger.info(f'Copying files to /home/worker/inputs...')
    not_done = True
    # while not_done:
    for file, size in input_files.items():
        path = os.path.join('/home/worker/inputs', file)
        logger.info(f'Checking file: {path}')
        if os.stat(path).st_size != size:
            logger.info(f'{path} size {os.stat(path).st_size} not equal tp {file} size {input_files.get(file)}')
            time.sleep(0.5)
            continue

    # for file in os.listdir('/home/worker/inputs'):
    #     path = os.path.join('/home/worker/inputs', file)
    #     if os.path.isdir(path):
    #         continue
    #     logger.info(f'Checking file: {path}')
    #     if int(os.stat(path).st_size) != int(input_files.get(file)):
    #         logger.info(f'{path} size {os.stat(path).st_size} not equal tp {file} size {input_files.get(file)}')
    #         time.sleep(0.5)
    #         continue
    #         not_done = False