<details>
<summary>We have moved to GitLab! Read this for more information.</summary>

We have recently moved our repositories to GitLab. You can find revpi-nodered
here: https://gitlab.com/revolutionpi/revpi-nodered  
All repositories on GitHub will stay up-to-date by being synchronised from
GitLab.

We still maintain a presence on GitHub but our work happens over at GitLab. If
you want to contribute to any of our projects we would prefer this contribution
to happen on GitLab, but we also still accept contributions on GitHub if you
prefer that.
</details>

# revpi-nodered

This repository contains the necessary files to have NodeRED running on the
RevPi.

## Makefile

- `build`: Runs `npm ci` to install dependencies from the lock file, 
  ensuring a clean, predictable state.
- `update-all`: Executes `npm update` to update all packages to the latest 
  versions allowed by the `package.json` constraints.
- `update-nodered`: Adds a target to check the current installed
  version of Node-RED against the latest available version. If the
  latest version is greater than the specified minimum version (3.1.9),
  it triggers an update.
- `start`: Installs dependencies and start the local Node-RED.

## Configuration

Certain configuration is needed to run NodeRED on the RevPi in an acceptable
manner. These are stored in the `config` directory.

### proxy-apache

The Apache2 configuration file in the folder "proxy-apache" is placed in the
folder "/etc/apache2/sites-available" on the Debian system. Subsequently, this
configuration is activated via `a2ensite revpi-nodered-proxy`, which is
activated by a `systemctl reload apache2` of Apache2.

Through this configuration, the certificates of the "RevPi-Cert-Wizard" are
applied to an SSL connection and Node-RED is secured by SSL via port 41880. For
this to work, the actual Node-RED server must be configured to the local IP
127.0.0.1 and port 1881. This ensures that Node-RED is not directly accessible
from the outside, but only via the Apache web server via SSL.

### systemd

The systemd Unit file starts the Node-RED service in the background as a
service. The service is bound to port 1881 on localhost 127.0.0.1. The packaging
would install the file "nodered.service" in "/lib/systemd/system", if this file
is installed manually, it should be stored in /etc/systemd/system".

The unit file prevades the user "nodered" on the system who has the home
directory "/var/lib/revpi-nodered." This user can be created as follows:

`adduser --system --home /var/lib/revpi-nodered --group nodered`

> If the user wants to use the RS485 interface with Node-RED, the group must be
> changed from "Group=nodered" to "Group=dialout" in the unit file.

#### Used sandbox techniques of systemd

The started process is secured by systemd, despite its own user, by securing
functions of systemd. The entire file system, except the paths "/dev", "/proc"
and "/sys", is read-only accessible for the process through the
"ProtectSystem=strict" parameter.

In order to give the user the possibility to write data via Node-RED, the home
directory is released again for write access by
"ReadWritePaths=/var/lib/revpi-nodered".

> The directory "/var/lib/revpi-nodered" is the only place where the process can
> write files.

The paths "/boot", "/home" and "/root" are completely blocked for all access for
the process. This is set via "InaccessiblePaths."

We have set further protect functions, which will be recommended when using
"[ProtectSystem](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#ProtectSystem=)".

- [ProtectControlGroups](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#ProtectControlGroups=)=yes
- [ProtectKernelModules](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#ProtectKernelModules=)=yes
- [ProtectKernelTunables](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#ProtectKernelTunables=)=yes
