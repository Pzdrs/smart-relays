import platform

PLATFORM = platform.system().lower()

DEBIAN = 'debian'
MAC = 'darwin'
RASPBERRY_PI = 'raspberry-pi'
UBUNTU = 'ubuntu'
WINDOWS = 'windows'

SUPPORTED_PLATFORMS = (RASPBERRY_PI,)
IS_LINUX = (PLATFORM == 'linux')
ON_SUPPORTED_PLATFORM = (PLATFORM in SUPPORTED_PLATFORMS)

if IS_LINUX:
    PLATFORM = platform.linux_distribution()[0].lower()
    if PLATFORM == DEBIAN:
        try:
            with open('/proc/cpuinfo') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('Hardware') and line.endswith('BCM2708'):
                        PLATFORM = RASPBERRY_PI
                        break
        except:
            pass