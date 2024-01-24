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
