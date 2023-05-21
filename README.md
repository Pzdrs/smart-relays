# Smart relays

Smart relays is a project that aims to provide a simple and easy to use web interface
for controlling relays and therefore devices connected to them.

## The stack

The core of the project is a Django application, written in Python, that provides an intuitive web interface
for controlling relays, and is backed by a SQLite database. The web interface is served by an Nginx web server,
background tasks are handled by Celery, which uses RabbitMQ as a message broker. The whole application is containerized
using Docker.

## Installation

The project is designed to be run exclusively on a Raspberry Pi. It was developed and tested on a Raspberry Pi 4.

1. Install pretty much any Linux distribution on your Raspberry Pi, that can run the Docker engine.
2. Install Docker and Docker Compose on your Raspberry Pi as described in the official documentation.
3. Use the provided `docker-compose.yml` file to start the application.
    - Docker will create a directory called **nginx**, where the provided `nginx.conf` file will be placed.
4. Restart the Nginx container so that it can pick up the new configuration using `docker restart smart-relays-nginx-1`

## Features

- [x] Support for multiple users
- [x] Per-relay user permissions
- [x] Per-relay audit logs
- [x] Three level permission system for shared relays
- [x] Scheduled tasks

## Time tracking

### Desktop: 68h

### Laptop: 14.25h