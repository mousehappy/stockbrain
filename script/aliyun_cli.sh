#!/usr/bin/sh

path=$(dirname $0)

src_path=${path%%script*}'src'
cm_path=$src_path'/crawler/base/CrawlerManager.py'

export_cmd='export PYTHONPATH='$src_path
$export_cmd
execute_cmd='python '$cm_path
$execute_cmd
