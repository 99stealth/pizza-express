#!/usr/bin/python

import time
import docker
import requests
import argparse
import re


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
    return requests.get('http://127.0.0.1:8081').status_code


def login_to_docker_registry(client, username, password, registry):
    response = client.login(username=username, password=password, registry=registry)
    return response


def push_docker_image(client, container_id, repository, tag='latest'):
    commit_id = client.commit(container=container_id, repository=repository, tag=tag)
    response = [line for line in client.push(repository, stream=True)]
    return commit_id, response


def stop_containers(client, *args):
    for container in args:
        client.stop(container=container)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Deployment automation with docker')
    parser.add_argument('-u', '--username', dest='username', type=str, required=True,
                        help='Username for docker registry')
    parser.add_argument('-p', '--password', dest='password', type=str, required=True,
                        help='Password for docker registry\'s account')
    parser.add_argument('-R', '--repository', dest='repository_name', required=True, type=str)
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true',
                        help='Activates verbose output')
    parser.add_argument('-r', '--registry', dest='docker_registry', type=str, default='hub.docker.com',
                        help='Docker registry you want to use')
    if not re.match('^[a-z0-9-_]+/[a-z0-9-_]+$', parser.parse_args().repository):
        print "[-] Repository {0} not match.".format(parser.parse_args().repository)
        exit(1)
    return parser.parse_args()


def main():
    args = parse_arguments()
    client = docker.Client(version='auto')
    needed_images = check_needed_images_exist(client)
    if needed_images:
        if args.verbose:
            print 'Need to pulling {0}'.format(needed_images)
        pull_docker_images(client, needed_images)

    redis_container_id, redis_container_name = run_redis_container(client)
    if args.verbose:
        print "Redis started with container ID {0} and names {1}".format(redis_container_id, redis_container_name)
    build_result = build_application_container(client)
    if args.verbose:
        print build_result[-1].split('"')[-2].replace('\\n', '')
    app_container_id = run_application_container(client, redis_container_name)
    time.sleep(5) # Waiting for deploy
    http_status = check_application_is_working()
    if http_status == 200:
        if args.verbose:
            print "HTTP status: {0}.".format(http_status)
        auth_data = login_to_docker_registry(client, args.username, args.password, args.docker_registry)
        commit_id, push_response = push_docker_image(client, app_container_id, args.repository_name)
        print "Commited: {0}".format(commit_id)
        stop_containers(client, app_container_id, redis_container_id)
    else:
        print "HTTP status: {0}. Please check container {1}".format(http_status, app_container_id)
        exit(2)


if __name__ == '__main__':
    main()

