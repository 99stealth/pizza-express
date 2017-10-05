import docker
import commands


def check_images(client, needed_imgs=['redis', 'node', 'nginx']):
    downloaded_images = []
    for container in client.images.list():
        downloaded_images.append(container.attrs["RepoTags"][0].split(":")[0])
    print downloaded_images
    print needed_imgs
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


def run_redis_container(client):
    pass

def check_application():
    pass

def send_docker_image():
    pass

def main():
    client = docker.from_env()
    check_images(client)
    redis_running = check_redis_running(client)
    print redis_running
    

if __name__ == '__main__':
    main()
