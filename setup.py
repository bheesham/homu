from setuptools import setup
import homu

setup_args= {
    'name': 'homu',
    'version': homu.version,
    'description': homu.description,
    'packages': [
        'homu'
    ],
    'data_files': [
        ('config', [
            'homu/scripts/static/cfg.toml.sample'
        ]),
        ('html', [
            'homu/scripts/static/html/index.html',
            'homu/scripts/static/html/queue.html'
        ])
    ],
    'scripts': [
        'homu/scripts/homu',
    ],
    'install_requires': [
        'click',
        'github3.py',
        'Jinja2',
        'requests',
        'toml'
    ]
}

setup(**setup_args)
