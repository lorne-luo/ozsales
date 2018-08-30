#!/bin/bash

mkdir -p ./testcode
for i in {1..100}
do
	wget http://www.one-express.cn/index.php/app/Index/verify -O ./testcode/$i.png
done
