{
    "DockerCollector": [

        {"docker_version": "Docker version 1.9.1, build a34a1d5"},

        {
            "59625b6296241a10dd49f2e128bebd44a7706774f542935e204908861b84361b": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "24 hours ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "ciqlq8sqdc2uvu39t73tlsupy",
                "id": "59625b6296241a10dd49f2e128bebd44a7706774f542935e204908861b84361b",
                "classname": "",
                "command": "\"/serviced/serviced-controller 5009czv7ag5fp8gxjmi0lsmq9 0 'su - zenoss -c \\\"/opt/zenoss/bin/zenactiond run -c --logfileonly --workerid $CONTROLPLANE_INSTANCE_ID \\\"'\"",
                "ports": ""
            },
            "523ba4421b206416118488367d97394024a6e671e0e97b2e1fdc1e226f42bb6c": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/opentsdb:latest",
                "title": "12rowggcjvanigl9x1afsaye5",
                "id": "523ba4421b206416118488367d97394024a6e671e0e97b2e1fdc1e226f42bb6c",
                "classname": "",
                "command": "\"/serviced/serviced-controller 7nvmcu10152b4wyp7ku9tn0js 0 '/bin/sh -c \\\" export CREATE_TABLES=1; /opt/opentsdb/start-opentsdb.sh localhost:2181,localhost:2182,localhost:2183\\\"'\"",
                "ports": "0.0.0.0:32794->4242/tcp"
            },
            "cb3d7325534168752f128a84325aa721235f4e4c08663202413f03e03cca8466": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "zenoss/serviced-isvcs:v40.1",
                "title": "serviced-isvcs_docker-registry",
                "id": "cb3d7325534168752f128a84325aa721235f4e4c08663202413f03e03cca8466",
                "classname": "",
                "command": "\"/bin/sh -c 'trap 'kill 0' 15; SETTINGS_FLAVOR=serviced exec /opt/registry/registry /opt/registry/registry-config.yml'\"",
                "ports": "0.0.0.0:5000->5000/tcp"
            },
            "04e4d2d88e278b6b37602e912f1ba35070dd9677a68e1a1da1b1beac16972733": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/hbase:latest",
                "title": "c0zm646f6evf7dcglir5lwatt",
                "id": "04e4d2d88e278b6b37602e912f1ba35070dd9677a68e1a1da1b1beac16972733",
                "classname": "",
                "command": "\"/serviced/serviced-controller 2otep9au6hd0tkwu93bvv2zvo 2 '/usr/bin/run-zk.sh /etc/zookeeper.cfg'\"",
                "ports": "0.0.0.0:32805->2183/tcp, 0.0.0.0:32804->2890/tcp, 0.0.0.0:32803->3890/tcp"
            },
            "85fa611801227171c90f2c5b180baa3bb48b3425a445b94ea868bf265d25580b": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "zenoss/serviced-isvcs:v40.1",
                "title": "serviced-isvcs_celery",
                "id": "85fa611801227171c90f2c5b180baa3bb48b3425a445b94ea868bf265d25580b",
                "classname": "",
                "command": "\"/bin/sh -c 'trap 'kill 0' 15; exec supervisord -n -c /opt/celery/etc/supervisor.conf'\"",
                "ports": ""
            },
            "0e10dcdb3683b9068d28fd06fd5290546e463a081c70006625e5d3c0c34d5719": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "23 hours ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "cqpnyttx798b3yiqmdvm45sju",
                "id": "0e10dcdb3683b9068d28fd06fd5290546e463a081c70006625e5d3c0c34d5719",
                "classname": "",
                "command": "\"/serviced/serviced-controller 78q9qxg1hbbpsnmnsyngmj7ug 0 'su - zenoss -c \\\"/opt/zenoss/bin/zencommand run -c --logfileonly --workers 1 --workerid $CONTROLPLANE_INSTANCE_ID --monitor localhost \\\"'\"",
                "ports": ""
            },
            "a7f55b84d8584d05d73614df8e76fd09d2f2ed70c7275140a953af3540f76c50": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "zenoss/isvcs-zookeeper:v3",
                "title": "serviced-isvcs_zookeeper",
                "id": "a7f55b84d8584d05d73614df8e76fd09d2f2ed70c7275140a953af3540f76c50",
                "classname": "",
                "command": "\"/bin/sh -c 'trap 'kill 0' 15; exec start-zookeeper'\"",
                "ports": "0.0.0.0:2181->2181/tcp, 0.0.0.0:2888->2888/tcp, 0.0.0.0:3888->3888/tcp, 127.0.0.1:12181->12181/tcp"
            },
            "a7654b9ec51ab51716b0d9b38f66030b5d28ed102aa5452da6b0b26b92120659": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "jw5knq4hxxz9zewluw35346z",
                "id": "a7654b9ec51ab51716b0d9b38f66030b5d28ed102aa5452da6b0b26b92120659",
                "classname": "",
                "command": "\"/serviced/serviced-controller 4rxt4leaibg2v106ngqy4case 0 'redis-server /etc/redis.conf & /bin/sh -c \\\"cd /opt/zenoss && exec ./zproxy/sbin/zproxy start\\\"'\"",
                "ports": "0.0.0.0:32779->8080/tcp"
            },
            "e5d7e7d9c8a1c42ade489b8a8d40db56d649e1aa95a3163c319bc8634f452830": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "1zzjiqg7itg0lquspc5oymbs7",
                "id": "e5d7e7d9c8a1c42ade489b8a8d40db56d649e1aa95a3163c319bc8634f452830",
                "classname": "",
                "command": "\"/serviced/serviced-controller 7t9argnozw4krv1zdk8a1mcqk 0 'su - zenoss -c \\\"cd /opt/zenoss && /bin/supervisord -n -c etc/metricshipper/supervisord.conf\\\"'\"",
                "ports": ""
            },
            "1c23b5b263db4465c0bb9ca89fd586547b78efe2dd1ea3497f4eb43f8eb10156": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "24 hours ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "28fvytdspbke0ztguil1kmomi",
                "id": "1c23b5b263db4465c0bb9ca89fd586547b78efe2dd1ea3497f4eb43f8eb10156",
                "classname": "",
                "command": "\"/serviced/serviced-controller b6qveplwjo1nr6w0vcqfk346r 0 'su - zenoss -c \\\"/opt/zenoss/bin/zenhub run -c --logfileonly --monitor localhost\\\"'\"",
                "ports": "0.0.0.0:32813->8081/tcp, 0.0.0.0:32812->8789/tcp"
            },
            "fe7f436b9c45e255ee5fe443d7c6ee3ab0f6ca1f3445ba6bbc09aea4ed018e46": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "6frfqqnjmsy9ba659p9tmolq2",
                "id": "fe7f436b9c45e255ee5fe443d7c6ee3ab0f6ca1f3445ba6bbc09aea4ed018e46",
                "classname": "",
                "command": "\"/serviced/serviced-controller ri18mhomy2m4amn6c0mvhd0h 0 'su - zenoss -c \\\"cd /opt/zenoss && /bin/supervisord -n -c etc/zauth/supervisord.conf\\\"'\"",
                "ports": "0.0.0.0:32797->9180/tcp"
            },
            "0e1871383e8a383624c6864111696c5986e3645a4b9ba17d3122217391390339": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "21 hours ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "1b7mn7bpdlb35f6xem9gc5pal",
                "id": "0e1871383e8a383624c6864111696c5986e3645a4b9ba17d3122217391390339",
                "classname": "",
                "command": "\"/serviced/serviced-controller b1critk14og5vhs34pvjc5ume 0 'su - zenoss -c \\\"/opt/zenoss/bin/zenpython run -c --logfileonly --workers 1 --workerid $CONTROLPLANE_INSTANCE_ID --monitor localhost \\\"'\"",
                "ports": ""
            },
            "a10f454c497ee23294d3ad2ff282a17dbebbc98e0c8439276ae8504cf49dcf27": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "bx71n07s3r4cdnbtofs7xd9x9",
                "id": "a10f454c497ee23294d3ad2ff282a17dbebbc98e0c8439276ae8504cf49dcf27",
                "classname": "",
                "command": "\"/serviced/serviced-controller 8shbx7ibstphxo1p43dyzosru 0 /usr/bin/mysqld_safe\"",
                "ports": "0.0.0.0:32792->3306/tcp"
            },
            "8b14e5f073c356049d578f4d32e2351f99968ecb061bf76d49b695cbb2f69640": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "24 hours ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "cz7r2m295gjelkmgz9o3svlp0",
                "id": "8b14e5f073c356049d578f4d32e2351f99968ecb061bf76d49b695cbb2f69640",
                "classname": "",
                "command": "\"/serviced/serviced-controller 57kf5gj6h93l3ysyebweq1nm3 0 'su - zenoss -c \\\"/opt/zenoss/bin/zenjobs run --logfileonly \\\"'\"",
                "ports": ""
            },
            "453a385bd3737c13e60451dd0eb5af2ebf3d1f0cb8074a6c2598067797a45458": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "a2iiu9kavlfi5und7fa2nc2mc",
                "id": "453a385bd3737c13e60451dd0eb5af2ebf3d1f0cb8074a6c2598067797a45458",
                "classname": "",
                "command": "\"/serviced/serviced-controller 740uds82y0ctuu9bazdzuqjzs 0 'su - zenoss -c \\\"cd /opt/zenoss && /bin/supervisord -n -c etc/metric-consumer-app/supervisord.conf\\\"'\"",
                "ports": "0.0.0.0:32771->8443/tcp"
            },
            "513fe03c37f4ac1ec5d07d3b42ed2f7e992f1c5d4c739c567ca052ea458fd84c": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "8dchwchjp7qdaouexvfc1syiv",
                "id": "513fe03c37f4ac1ec5d07d3b42ed2f7e992f1c5d4c739c567ca052ea458fd84c",
                "classname": "",
                "command": "\"/serviced/serviced-controller d7e3oq9d8pxjhy99vb1vg7cry 0 /usr/bin/mysqld_safe\"",
                "ports": "0.0.0.0:32781->3306/tcp"
            },
            "3e9b8f068e63c716cdf45cb2fd040e451be638d3d6cbb14353105949bbfe6e14": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "264t4yqjl7wnubjn0kr2lh9zw",
                "id": "3e9b8f068e63c716cdf45cb2fd040e451be638d3d6cbb14353105949bbfe6e14",
                "classname": "",
                "command": "\"/serviced/serviced-controller bedabpuaqgpybynffnwcijdt 0 'su - zenoss -c \\\"/opt/zenoss/bin/zenjserver run -c --logfileonly \\\"'\"",
                "ports": "0.0.0.0:32793->8700/tcp"
            },
            "d743f38ec0cddd33c991c15e1ac80c6b95a49f45e52266259d5dcdbabbc2765a": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "4hbkst5xihr318anj1y6gkm5c",
                "id": "d743f38ec0cddd33c991c15e1ac80c6b95a49f45e52266259d5dcdbabbc2765a",
                "classname": "",
                "command": "\"/serviced/serviced-controller aiaw8iq2sw92z6d6in4a6tnvf 0 'su - zenoss -c \\\"cd /opt/zenoss && /bin/supervisord -n -c etc/central-query/supervisord.conf\\\"'\"",
                "ports": "0.0.0.0:32784->8888/tcp"
            },
            "822ab0b1f4db601681d66c9d1dc73770fa69f16d51bd88193ed7b0f6bd4e0226": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "tdkohwftyebxqgy0sldpgtmu",
                "id": "822ab0b1f4db601681d66c9d1dc73770fa69f16d51bd88193ed7b0f6bd4e0226",
                "classname": "",
                "command": "\"/serviced/serviced-controller 8uv24hue6ugwabjhamci8k2ag 0 'su - zenoss -c \\\"/bin/supervisord -n -c /opt/zenoss/etc/zminion/supervisord.conf\\\"'\"",
                "ports": ""
            },
            "6d02294336af686c21ab8a36d23bae5c7dc698203909743575cfa2f7e52f9331": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "zenoss/serviced-isvcs:v40.1",
                "title": "serviced-isvcs_logstash",
                "id": "6d02294336af686c21ab8a36d23bae5c7dc698203909743575cfa2f7e52f9331",
                "classname": "",
                "command": "\"/bin/sh -c 'trap 'kill 0' 15; exec /opt/logstash-1.4.2/bin/logstash agent -f /usr/local/serviced/resources/logstash/logstash.conf'\"",
                "ports": "0.0.0.0:5042-5043->5042-5043/tcp, 127.0.0.1:9292->9292/tcp"
            },
            "20fab7de800b6323605d57d2826aac2146a08165d8c62e246f06d265540d0a21": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "24 hours ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "bafoag2lu1a1zprivci3nh4v2",
                "id": "20fab7de800b6323605d57d2826aac2146a08165d8c62e246f06d265540d0a21",
                "classname": "",
                "command": "\"/serviced/serviced-controller 50dcksc4heovk6a8790yd89rd 0 'su - zenoss -c \\\"/opt/zenoss/bin/zopectl fg\\\" '\"",
                "ports": "0.0.0.0:32811->9080/tcp"
            },
            "7d4438367a16105df4b23dcdf6bb442e46cbf3be310daa6ece0b79bc9bef9469": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/hbase:latest",
                "title": "2dj36bextiqvi84i2inyn7gzg",
                "id": "7d4438367a16105df4b23dcdf6bb442e46cbf3be310daa6ece0b79bc9bef9469",
                "classname": "",
                "command": "\"/serviced/serviced-controller 2otep9au6hd0tkwu93bvv2zvo 1 '/usr/bin/run-zk.sh /etc/zookeeper.cfg'\"",
                "ports": "0.0.0.0:32790->2182/tcp, 0.0.0.0:32789->2889/tcp, 0.0.0.0:32788->3889/tcp"
            },
            "14974bc3031930139bbb18b4f16a082a305aa8906f55cd77aebcd91065f93950": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "24 hours ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "9u1318c4qevp0ma5rxrqdgwpj",
                "id": "14974bc3031930139bbb18b4f16a082a305aa8906f55cd77aebcd91065f93950",
                "classname": "",
                "command": "\"/serviced/serviced-controller 3rstr9gt8rtgm0xns4xr2zkr9 0 'su - zenoss -c \\\"/usr/bin/nice -n 10 /opt/zenoss/bin/zeneventd run -c --logfileonly \\\"'\"",
                "ports": ""
            },
            "dfc0beb3f55fb8283c604c8fdf05d97e5b19845c35063268159e6cf6af925f2f": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "9ww06k1xbxyj6yni7lf9wjny6",
                "id": "dfc0beb3f55fb8283c604c8fdf05d97e5b19845c35063268159e6cf6af925f2f",
                "classname": "",
                "command": "\"/serviced/serviced-controller 368xyn2hhfsqt675autj7hv4v 0 'su - zenoss -c \\\"cd /opt/zenoss && /bin/supervisord -n -c etc/metricshipper/supervisord.conf\\\"'\"",
                "ports": ""
            },
            "f21971a5e25ee15b409de972e9faeb07b60196c88933c71a49989303ea32a161": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "46ipmdev3cw3owjve4biqyhns",
                "id": "f21971a5e25ee15b409de972e9faeb07b60196c88933c71a49989303ea32a161",
                "classname": "",
                "command": "\"/serviced/serviced-controller 4fjja82pnug9slp9av694g2rh 0 '/usr/bin/redis-server /etc/redis.conf'\"",
                "ports": "0.0.0.0:32780->6379/tcp"
            },
            "68887f1a9be5c23974a6f3e4fe57f22a8a1828e36d80b945a15783e90a04520a": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "zenoss/serviced-isvcs:v40.1",
                "title": "serviced-isvcs_elasticsearch-logstash,serviced-isvcs_logstash/elasticsearch",
                "id": "68887f1a9be5c23974a6f3e4fe57f22a8a1828e36d80b945a15783e90a04520a",
                "classname": "",
                "command": "\"/bin/sh -c 'trap 'kill 0' 15; exec /opt/elasticsearch-1.3.1/bin/elasticsearch -Des.node.name=elasticsearch-logstash  -Des.cluster.name=4p9oz1yeejh79bfkr1juawn6x '\"",
                "ports": "127.0.0.1:9100->9100/tcp"
            },
            "033263de5f5789057724580e3c7ebc556e3827eb2cc9af436b0688588d2c471e": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/opentsdb:latest",
                "title": "2lim1utmu888pobsfhrdca9w8",
                "id": "033263de5f5789057724580e3c7ebc556e3827eb2cc9af436b0688588d2c471e",
                "classname": "",
                "command": "\"/serviced/serviced-controller 8iyy23f51wgfv03eq28zwqla5 0 '/opt/opentsdb/start-opentsdb.sh localhost:2181,localhost:2182,localhost:2183'\"",
                "ports": "0.0.0.0:32798->4242/tcp"
            },
            "fbae9446b2b28a3a541acfa2917d8e162119f4661ae5c36344912c61021faf69": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/hbase:latest",
                "title": "1hw9yrrwrpx6rfxwif2oc2w19",
                "id": "fbae9446b2b28a3a541acfa2917d8e162119f4661ae5c36344912c61021faf69",
                "classname": "",
                "command": "\"/serviced/serviced-controller 5xd1na3kyyskesjsm7o5l2pw9 1 '/usr/bin/run-hbase-regionserver.sh /etc/hbase-site.xml $CONTROLPLANE_INSTANCE_ID'\"",
                "ports": "0.0.0.0:32800->60201/tcp, 0.0.0.0:32799->60301/tcp"
            },
            "451f1db5b57e77349c72ea676bdd7c5ee915996eae10550732c3fd7651a4326a": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/hbase:latest",
                "title": "av53onrl40hibiuzxdx7qd32s",
                "id": "451f1db5b57e77349c72ea676bdd7c5ee915996eae10550732c3fd7651a4326a",
                "classname": "",
                "command": "\"/serviced/serviced-controller 5xd1na3kyyskesjsm7o5l2pw9 0 '/usr/bin/run-hbase-regionserver.sh /etc/hbase-site.xml $CONTROLPLANE_INSTANCE_ID'\"",
                "ports": "0.0.0.0:32796->60200/tcp, 0.0.0.0:32795->60300/tcp"
            },
            "cc390329f8d9b1637abd03b573b0844aaf739344bb9d056c3b469a0226e23941": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "5p8xwopkrmdbgyhknh8if1sfs",
                "id": "cc390329f8d9b1637abd03b573b0844aaf739344bb9d056c3b469a0226e23941",
                "classname": "",
                "command": "\"/serviced/serviced-controller amjqdhzn2y26665x9d03b14ce 0 'su - zenoss -c \\\"export DEFAULT_ZEP_JVM_ARGS='-server -Xmx4294967296' && /opt/zenoss/bin/zeneventserver run_quiet \\\"'\"",
                "ports": "0.0.0.0:32802->8084/tcp"
            },
            "23cdc052edf9111a38b7a7f70bb6ea11ceb2dd4e758f167323721fb68e28e563": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/hbase:latest",
                "title": "ci67emyceslulkj1v5vqxl9qf",
                "id": "23cdc052edf9111a38b7a7f70bb6ea11ceb2dd4e758f167323721fb68e28e563",
                "classname": "",
                "command": "\"/serviced/serviced-controller 2otep9au6hd0tkwu93bvv2zvo 0 '/usr/bin/run-zk.sh /etc/zookeeper.cfg'\"",
                "ports": "0.0.0.0:32778->2181/tcp, 0.0.0.0:32777->2888/tcp, 0.0.0.0:32776->3888/tcp"
            },
            "98c0f7738affaa41d49337c1acda281b09e0dfbe319eab14422c735245a38079": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/hbase:latest",
                "title": "edjp7wmalqji6ysfojrn7gz4",
                "id": "98c0f7738affaa41d49337c1acda281b09e0dfbe319eab14422c735245a38079",
                "classname": "",
                "command": "\"/serviced/serviced-controller 5xd1na3kyyskesjsm7o5l2pw9 2 '/usr/bin/run-hbase-regionserver.sh /etc/hbase-site.xml $CONTROLPLANE_INSTANCE_ID'\"",
                "ports": "0.0.0.0:32783->60202/tcp, 0.0.0.0:32782->60302/tcp"
            },
            "26bc13ab655f93713a48bda66fd292077492efece4a87937297eab50146d405b": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "9pj3kqeey2dxy4cgggi4d1cet",
                "id": "26bc13ab655f93713a48bda66fd292077492efece4a87937297eab50146d405b",
                "classname": "",
                "command": "\"/serviced/serviced-controller 9wy6sv05xexnn4gjp2lwnp5er 0 '/usr/bin/redis-server /etc/redis.conf'\"",
                "ports": "0.0.0.0:32791->6379/tcp"
            },
            "f85804cef1f19e2247e7bff4b3ec1160ee0f28790be59d2058f3ee8170b71e4a": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/hbase:latest",
                "title": "4qfj0rbh0yr42vywdxlufcl1y",
                "id": "f85804cef1f19e2247e7bff4b3ec1160ee0f28790be59d2058f3ee8170b71e4a",
                "classname": "",
                "command": "\"/serviced/serviced-controller 2wxi0x6aglu0w8wbjd38au6nl 0 '/usr/bin/run-hbase-master.sh /etc/hbase-site.xml'\"",
                "ports": "0.0.0.0:32787->60000/tcp, 0.0.0.0:32786->60010/tcp, 0.0.0.0:32785->61000/tcp"
            },
            "2de1339742a1a7379bcccf533dae3f385ea0a8b59e39037aeb5202ecd3e54407": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "zenoss/serviced-isvcs:v40.1",
                "title": "serviced-isvcs_opentsdb",
                "id": "2de1339742a1a7379bcccf533dae3f385ea0a8b59e39037aeb5202ecd3e54407",
                "classname": "",
                "command": "\"/bin/sh -c 'trap 'kill 0' 15; cd /opt/zenoss && exec supervisord -n -c /opt/zenoss/etc/supervisor.conf'\"",
                "ports": "0.0.0.0:4242->4242/tcp, 127.0.0.1:8888->8888/tcp, 127.0.0.1:9090->9090/tcp, 127.0.0.1:58443->58443/tcp, 0.0.0.0:8443->8443/tcp, 127.0.0.1:58888->58888/tcp"
            },
            "c94d08ee1b7893652e25d7f14c5aa80323ab29655309673783648d86850e1a45": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "zenoss/serviced-isvcs:v40.1",
                "title": "serviced-isvcs_elasticsearch-serviced",
                "id": "c94d08ee1b7893652e25d7f14c5aa80323ab29655309673783648d86850e1a45",
                "classname": "",
                "command": "\"/bin/sh -c 'trap 'kill 0' 15; exec /opt/elasticsearch-0.90.9/bin/elasticsearch -f -Des.node.name=elasticsearch-serviced  -Des.cluster.name=545sbgwvt4idanwml3bewmfzp '\"",
                "ports": "127.0.0.1:9200->9200/tcp"
            },
            "7b2380202d8c114590417d7c0706480b00ca9e2a89ad722ec95de8800a8d0940": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "d2vpndyu8k3c3b5w153rcivdh",
                "id": "7b2380202d8c114590417d7c0706480b00ca9e2a89ad722ec95de8800a8d0940",
                "classname": "",
                "command": "\"/serviced/serviced-controller 7sexasmop90cgqgk787f4ehma 0 /usr/sbin/rabbitmq-server\"",
                "ports": "0.0.0.0:32775->4369/tcp, 0.0.0.0:32774->5672/tcp, 0.0.0.0:32773->15672/tcp, 0.0.0.0:32772->44001/tcp"
            },
            "1fe35e4c6605a1765b37ca7c340432538ab8dde76df5ab37bbdd16954a31a649": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "23 hours ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "ajfug0o4l1ubuxeb5i2jjd4s8",
                "id": "1fe35e4c6605a1765b37ca7c340432538ab8dde76df5ab37bbdd16954a31a649",
                "classname": "",
                "command": "\"/serviced/serviced-controller bdtnyolxgolypoiugqyy49zga 0 'su - zenoss -c \\\"/opt/zenoss/bin/zenucsevents run -c --logfileonly --workers 1 --workerid $CONTROLPLANE_INSTANCE_ID --monitor localhost \\\"'\"",
                "ports": ""
            },
            "58ef07c1d463172e08563670bd999c4f2ba9c4156277124db7f45d2f16a6c766": {
                "modname": "ZenPacks.zenoss.Docker.DockerContainer",
                "compname": "",
                "created": "3 days ago",
                "image": "localhost:5000/4rxt4leaibg2v106ngqy4case/devimg:latest",
                "title": "coegxsv184ivlaf8c7nnq8xjs",
                "id": "58ef07c1d463172e08563670bd999c4f2ba9c4156277124db7f45d2f16a6c766",
                "classname": "",
                "command": "\"/serviced/serviced-controller 9al09pov38cuwoto2arvg6wtp 0 '/bin/memcached -u nobody -v -m 922'\"",
                "ports": "0.0.0.0:32768->11211/tcp"
            }
        }
    ]
}
