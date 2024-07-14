import subprocess

with open('installed_packages.txt') as f:
    packages = f.read().splitlines()

for package in packages:
    package_name = package.split('==')[0]
    subprocess.call(['pip', 'uninstall', '-y', package_name])
