## Verify if Xdebug is Installed
Check if you already have Xdebug installed using the Xdebug setup wizard at https://xdebug.org/wizard. Follow the instructions provided after pasting your phpinfo() output.

## Instructions to Set Up Xdebug

1. Download xdebug. Download the version of Xdebug recommended by the Xdebug setup wizard.
2. Install the pre-requisites for compiling PHP extensions. These packages are often called 'php-dev', or 'php-devel', 'automake' and 'autoconf'.
```
sudo apt-get install php-dev autoconf automake
```
3. Unpack the downloaded file
```
tar -xvzf xdebug-[version].tgz
```
4. Navigate to the Xdebug Directory
```
cd xdebug-[version]
```
5. Run phpize
```
/opt/lampp/bin/phpize
```
6. Configure
```
./configure --with-php-config=/opt/lampp/bin/php-config
```
7. Compile
```
make
```
8. Copy the Compiled File
```
cp modules/xdebug.so [Extensions directory]
```
9. Update php.ini
Open the file /opt/lampp/etc/php.ini and add the following lines at the end:
```
[xdebug]
zend_extension="[Extensions directory]/xdebug.so"
xdebug.start_upon_error = yes
xdebug.client_port = 9003
xdebug.mode=debug
xdebug.client_host=localhost
```
10. Restart the Apache Webserver
```
sudo /opt/lampp/lampp restart
```

## Configure VSCode
1. Set the PHP Executable Path
Open VSCode settings and add the following settings:
```
"php.validate.executablePath": "C:\\xampp\\php\\php.exe",
"php.debug.executablePath": "C:\\xampp\\php\\php.exe"
```
2. Create a Launch File
In VSCode, create or update a launch file (launch.json) with the following content:
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Listen for Xdebug",
            "type": "php",
            "request": "launch",
            "port": 9003
        }
    ]
}
```

