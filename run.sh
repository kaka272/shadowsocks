#!/bin/bash

set -ex

login_url="https://dashboard.cpolar.com/login"
status_url="https://dashboard.cpolar.com/status"
cookies_file="/Users/tellme/Shadowsocks/cookies.txt"


csrf_token=$(curl $login_url | grep -o '<input type="hidden" name="csrf_token" value="[^"]*"' | awk -F'value="' '{print $2}' | awk -F'"' '{print $1}')

echo "CSRF Token: $csrf_token"


csrf_token="\"$csrf_token\""
quote_cmd="python2 -c 'import urllib; print urllib.quote(${csrf_token})'"
csrf_token=$(eval $quote_cmd)
echo "Quote CSRF Token: $csrf_token"


read -s -p "请输入密码: " passwd

passwd="\"$passwd\""
quote_cmd="python2 -c 'import urllib; print urllib.quote(${passwd})'"
passwd=$(eval $quote_cmd)


cmd_str="login=1028265636%40qq.com&password=$passwd&csrf_token=$csrf_token"


curl -X POST -c $cookies_file -d "$cmd_str" $login_url
tunnel_string=$(curl -b $cookies_file $status_url | grep -m1 -oE 'tcp://[^:]+:[0-9]+')


url=$(echo $tunnel_string | sed -E 's/tcp:\/\/([^:]+):[0-9]+/\1/')
port=$(echo $tunnel_string | sed -E 's/tcp:\/\/[^:]+:([0-9]+)/\1/')


echo "URL: $url"
echo "Port: $port"


python2 local.py -s $url -p $port -l 1086 -k hello


