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
- [ ] Audit log coverage for relay sharing
### Must haves
- [x] Support for multiple users
- [x] Per-relay user permissions
- [x] Per-relay audit logs
- [x] Three level permissions for shared relays
- [ ] Scheduled tasks
- [ ] Built-in HTTP API
- [x] Audit log pagination - both global and in relay detail
### Shit to fix
- Show more kind of pagination jede do nekonecna, musim tam dat nejakej cap
## Time tracking
### Desktop: 53.5h
### Laptop: 14.25h