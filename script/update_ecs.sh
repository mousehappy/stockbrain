#!/usr/bin/sh

path=$(dirname $0)
src_dir=${path%%script*}
cd $src_dir
git pull

src_path=$src_dir'src'
source_cmd='source '$src_dir'.venv/bin/activate'
cm_path=$src_path'/crawler/base/CrawlerManager.py'

#启用venv
echo $source_cmd
$source_cmd

#安装python包
pip install -r resource/centos7_requirement

#设置环境变量
export_cmd='export PYTHONPATH='$src_path
$export_cmd

#执行crawl
execute_cmd='python '$cm_path
$execute_cmd
