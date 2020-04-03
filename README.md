# Install Mattermost via Bundlewrap

Small bundle to install Mattermost on your server.

## Config Example
```json
'mattermost': {
    'version': '5.21.0',
    'checksum': '909b17498139cd511d4e5483e2b7be0b757ac28ea5063be9c3d82cbe49b4a696',
    'site_url': 'https://example.org',
    'site_name': 'Example.org - Mattermost',
    'brand': 'Example Org',
    'description': 'Powered by DasLampe',
    'brand_image': False,
    'email': {
        'server': 'mail.example.org',
        'port': '587',
        'security': 'STARTTLS',

        'feedback_name': 'DasLampe',
        'feedback_email': 'feedback@example.org',
        'feedback_org': 'Example Org',
        'reply_to': 'daslampe@example.org',
    },
    'allow_cros_from': 'example.org example.org:443',
}
```

## License
See LICENSE

## Suggestions
- Use proxy to access your Mattermost Instance, and enable SSL!
- Disable direct access to Mattermost instance