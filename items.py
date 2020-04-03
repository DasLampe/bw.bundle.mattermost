global repo, node


database_password = repo.vault.password_for("postgres_mattermost_user{}".format(node.name))
mattermost_config = node.metadata.get('mattermost', {})

postgres_roles = {
    'mattermost': {
        'superuser': False,
        'password': database_password,
    }
}

postgres_dbs = {
    "mattermost": {
        "owner": "mattermost",
        "when_creating": {
            "encoding": "UTF-8",
        },
    },
}

downloads = {
    '/tmp/mattermost.tar.gz': {
        'url': "https://releases.mattermost.com/{version}/mattermost-{version}-linux-amd64.tar.gz".format(version=node.metadata.get('mattermost', {}).get('version', '5.21.0')),
        'sha256': node.metadata.get('mattermost', {}).get('checksum', '909b17498139cd511d4e5483e2b7be0b757ac28ea5063be9c3d82cbe49b4a696'),
    }
}

actions = {
    'extract_mattermost': {
        'command': 'tar xfvz /tmp/mattermost.tar.gz -C /opt/',
        'needs': [
            'download:/tmp/mattermost.tar.gz',
        ],
    },
}

directories = {
    '/opt/mattermost/data': {
        'needs': [
            'action:extract_mattermost',
        ],
    },
}

files = {
    '/opt/mattermost/config/config.json': {
        'source': 'opt/mattermost/config/config.json',
        'content_type': 'mako',
        'context': {
            'dbpassword': database_password,
            'site_url': mattermost_config.get('site_url', ''),
            'site_name': mattermost_config.get('site_name', ''),
            'brand_text': mattermost_config.get('brand', ''),
            'description_text': mattermost_config.get('description', ''),
            'smtp_server': mattermost_config.get('email', {}).get('server', ''),
            'smtp_port': mattermost_config.get('email', {}).get('port', '587'),
            'smtp_connection_security': mattermost_config.get('email', {}).get('security', 'STARTTLS'),
            'allow_cors_from': mattermost_config.get('allow_cors_from', ''),
            'feedback_email': mattermost_config.get('email', {}).get('feedback_mail', ''),
            'feedback_name': mattermost_config.get('email', {}).get('feedback_name', ''),
            'feedback_org': mattermost_config.get('email', {}).get('feedback_org', ''),
            'reply_to': mattermost_config.get('email', {}).get('reply_to', ''),
            'elastic_password': repo.vault.password_for('elasticsearch_for_mattermost_on_{}'.format(node.name))
        },
        'needs': [
           'action:extract_mattermost',
        ],
        'triggers': [
            'svc_systemd:mattermost.service:reload',
        ],
    },
    '/lib/systemd/system/mattermost.service': {
        'source': 'lib/systemd/system/mattermost.service',
        'needs': [
            'file:/opt/mattermost/config/config.json',
        ]
    },
}

if mattermost_config.get('brand_image', False):
    files['/opt/mattermost/data/brand/image.png'] = {
        'source': 'image.png',
        'unless': "test -e /opt/mattermost/data/brand/image.png"
    }

svc_systemd = {
    'mattermost.service': {
        'enabled': True,
        'running': True,
        'needs': [
            'file:/lib/systemd/system/mattermost.service',
        ],
    },
}


