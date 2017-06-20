from setuptools import setup, find_packages

try:
    setup(
        name = "baseride-django-billing",
        packages = find_packages(),
        install_requires = [
            "django-jsonfield >= 0.5.7",
            "django >= 1.11",
        ],
        version = "1.0.3",
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Framework :: Django",
        ]
    )
finally:
    pass
