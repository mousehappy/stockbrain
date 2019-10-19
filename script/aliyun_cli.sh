#!/usr/bin/sh

path=$(dirname $0)

src_path=${path%%script*}'src'
source_cmd='source '${path%%script*}'.venv/bin/activate'
cm_path=$src_path'/crawler/base/CrawlerManager.py'

echo $source_cmd
$source_cmd

export_cmd='export PYTHONPATH='$src_path
$export_cmd
execute_cmd='python '$cm_path
$execute_cmd
