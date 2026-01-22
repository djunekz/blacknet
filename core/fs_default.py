def default_fs():
    return {
        "/": {
            "home": {},
            "etc": {},
            "var": {}
        },

        "/home": {
            "admin": {}
        },

        "/home/admin": {
            ".bash_history": "ssh root@127.0.0.1\nsudo reboot\n"
        },

        "/etc": {
            "passwd": (
                "root:x:0:0:root:/root:/bin/bash\n"
                "admin:x:1000:1000:admin:/home/admin:/bin/bash\n"
            ),
            "shadow": "root:$6$hash:19000:0:99999:7:::",
            "ssh_config": "PermitRootLogin yes"
        },

        "/var": {
            "log": {}
        },

        "/var/log": {
            "auth.log": ""
        }
    }
