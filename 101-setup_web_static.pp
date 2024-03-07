#!/usr/bin/puppet apply
# Script that sets up your web servers for the deployment of web_static
exec { 'update-apt':
  command => '/usr/bin/apt-get update',
  path    => '/usr/bin:/usr/sbin:/bin',
}

exec { 'remove-current-directory':
  command => 'rm -rf /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
}

package { 'nginx-package':
  ensure  => installed,
  require => Exec['update-apt'],
}

file { '/var/www-root':
  ensure  => directory,
  mode    => '0755',
  recurse => true,
  require => Package['nginx-package'],
}

file { '/var/www-root/html/index.html':
  content => 'Hello, World!',
  require => File['/var/www-root'],
}

file { '/var/www-root/error/404.html':
  content => "Ceci n'est pas une page",
  require => File['/var/www-root'],
}

exec { 'create-static-folders':
  command => 'mkdir -p /data/web_static/releases/test /data/web_static/shared',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => Package['nginx-package'],
}

file { '/data/web_static/releases/test/index.html':
  content =>
"<!DOCTYPE html>
<html lang='en-US'>
	<head>
		<title>Home - AirBnB Clone</title>
	</head>
	<body>
		<h1>Welcome to AirBnB!</h1>
	</body>
</html>
",
  replace => true,
  require => Exec['create-static-folders'],
}

exec { 'link-static-files-folder':
  command => 'ln -sf /data/web_static/releases/test/ /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => [
    Exec['remove-current-directory'],
    File['/data/web_static/releases/test/index.html'],
  ],
}

exec { 'change-data-owner':
  command => 'chown -hR ubuntu:ubuntu /data',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => Exec['link-static-files-folder'],
}

file { '/etc/nginx/default-site':
  ensure  => present,
  mode    => '0644',
  content =>
"server {
	listen 80 default_server;
	listen [::]:80 default_server;
	server_name _;
	index index.html index.htm;
	error_page 404 /404.html;
	add_header X-Served-By \$hostname;
	location / {
		root /var/www-root/html/;
		try_files \$uri \$uri/ =404;
	}
	location /hbnb_static/ {
		alias /data/web_static/current/;
		try_files \$uri \$uri/ =404;
	}
	if (\$request_filename ~ redirect_me){
		rewrite ^ https://sketchfab.com/bluepeno/models permanent;
	}
	location = /404.html {
		root /var/www-root/error/;
		internal;
	}
}",
  require => [
    Package['nginx-package'],
    File['/var/www-root/html/index.html'],
    File['/var/www-root/error/404.html'],
    Exec['change-data-owner'],
  ],
}

exec { 'enable-default-site':
  command => "ln -sf '/etc/nginx/default-site' '/etc/nginx/sites-enabled/default-site'",
  path    => '/usr/bin:/usr/sbin:/bin',
  require => File['/etc/nginx/default-site'],
}

exec { 'restart-nginx':
  command => 'sudo service nginx restart',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => [
    Exec['enable-default-site'],
    Package['nginx-package'],
    File['/data/web_static/releases/test/index.html'],
  ],
}

Exec['restart-nginx']
