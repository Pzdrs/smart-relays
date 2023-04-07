# Smart relays
Smart relays is a project that aims to provide a simple and easy to use web interface 
for controlling relays and therefore devices connected to them.
## Installation
## The stack
The core of the project is a Django application, written in Python, that provides an intuitive web interface
for controlling relays, and is backed by a SQLite database. The built-in HTTP API allows
for easy integration with other applications, such as **Node-RED** or **Home Assistant**
## Features
### Nice to haves
- [ ] MQTT support
- [ ] Websocket based reactive UI
### Must haves
- [ ] Support for multiple users
- [ ] Per-relay user permissions
- [x] Per-relay audit logs
- [ ] Scheduled tasks
- [ ] Built-in HTTP API