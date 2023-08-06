import platform

PLATFORM = platform.system().lower()

DEBIAN = 'debian'
MAC = 'darwin'
RASPBERRY_PI = 'raspberry-pi'
UBUNTU = 'ubuntu'
WINDOWS = 'windows'

SUPPORTED_PLATFORMS = (RASPBERRY_PI,)
IS_LINUX = (PLATFORM == 'linux')

if IS_LINUX:
    try:
        with open('/proc/cpuinfo') as f:
            for line in f:
                line = line.strip()
                print(line)
                if line.startswith('Model') and 'raspberry' in line.lower():
                    print('hit')
                    PLATFORM = RASPBERRY_PI
                    break
    except:
        pass

ON_SUPPORTED_PLATFORM = (PLATFORM in SUPPORTED_PLATFORMS)
