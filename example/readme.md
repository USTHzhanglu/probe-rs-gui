# Readme

how to use

## *.bin

烧录所用到的固件

## *.yaml

烧录算法文件，Keil补丁包。文件名需要与yaml中对应
通过[`target-gen`](https://github.com/probe-rs/probe-rs/tree/master/target-gen#target-gen)生成

`target-gen pack xxx.pack ./`

## config.yaml

配置文件，描述了目标芯片型号，烧录算法所在位置，烧录速率等

```yaml
chip: HC32F4A0PGTB
pack_yaml: ./HC32F4A0-Series.yaml
speed: '16000'
```
