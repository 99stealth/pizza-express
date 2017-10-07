#!/usr/bin/python

import docker

def check_needed_images_exist(client, needed_imgs=['redis:latest', 'node:latest']):
    docker_images = []
    need_to_pull = []
    for image in client.images():
        docker_images.append(image["RepoTags"][0])

    for image in needed_imgs:        
        if image not in docker_images:
             need_to_pull.append(image)

    return need_to_pull

def pull_docker_images(client, need_to_pull):
    for image in need_to_pull:
        client.pull(image)

def run_redis_container(client, image='redis:latest'):
    config = client.create_host_config(port_bindings={'6379': '6379'})
    container = client.create_container(image=image, host_config=config)
    response = client.start(container=container.get('Id'))
    for started_container in client.containers():
        if started_container['Id'] == container['Id']:
            return started_container['Id'], started_container['Names'][0].replace("/", "")
        else:
            continue

def build_application_container(client, tag='pizza-express'):
    response = [line for line in client.build(tag=tag, path='./')]
    return response
    
def run_application_container(client, redis_container_name, image='pizza-express:latest'):
    config = client.create_host_config(port_bindings={'3000': '8081'}, links=[(redis_container_name, 'redis')])
    container = client.create_container(image=image, host_config=config)
    response = client.start(container=container.get('Id'))
    return container

def check_application_is_working():
    pass

def send_docker_image():
    pass

def main():
    client = docker.Client(version='auto')
    needed_images = check_needed_images_exist(client)
    if needed_images:
        pull_docker_images(client, needed_images)

    redis_container_id, redis_container_name = run_redis_container(client)
#   print redis_container_id, redis_container_name
    build_result = build_application_container(client)
    app_container_id = run_application_container(client, redis_container_name) 
#   print build_result[-1].split('"')[-2].replace('\\n', '') 
            
if __name__ == '__main__':
    main()
