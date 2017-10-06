#!/usr/bin/python

import docker
import commands


def check_images(client, needed_imgs=['redis', 'node']):
    downloaded_images = []
    for image in client.images.list():
        print image
        downloaded_images.append(image.attrs["RepoTags"][0].split(":")[0])

    for image in needed_imgs:
        if image not in downloaded_images:
            print "[!] Pulling {0} container".format(image)
            client.images.pull('{0}:latest'.format(image))
        else:
            print "[+] Image {0} is present".format(image)

def check_redis_running(client, redis_container_name='redis'):
    ran_containers = []
    containers_list = client.containers.list()
    for container in containers_list:
        ran_containers.append(container.attrs['Name'].split('/')[1])
    if redis_container_name in ran_containers:
        return True
    else:
        return False

def run_tests():
    pass


def run_redis_container():
    output = commands.getstatusoutput('docker run -d --name redis -p 6379:6379 redis')
    return output

def run_container(**kwargs):
    if not kwargs['image']:
        print "[-] Print please provide container name"
        exit(1)
    
    if kwargs['container_port'] and kwargs['host_port']:
        
    output = commands.getstatusoutput()

def run_unittests():
    output = commands.getstatusoutput('npm test')
    return output

def run_container_with_application():

def send_docker_image():
    pass

def main():
    client = docker.from_env(version='auto')
    check_images(client)
    redis_running = check_redis_running(client)
    if not redis_running:
        redis = run_redis_container()
    unittests_passed = run_unittests()
    if unittests_passed[0] == 0:
            
    

if __name__ == '__main__':
    main()
