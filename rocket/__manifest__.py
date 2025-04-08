{
    'name': 'Rocket Landing Page',
    'version': '16.0.1.0.0',
    'summary': 'Landing page with a flying rocket animation.',
    'author': 'Your Name or Company',
    'website': 'https://yourwebsite.com',
    'category': 'Website',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        'views/rocket_landing_page.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/rocket/static/src/js/rocket.esm.js',
            '/rocket/static/src/scss/rocket.scss',
        ],
    },
}
