# Readme

how to use

## *.yaml

烧录算法文件，Keil补丁包。文件名需要与yaml中对应
通过[`target-gen`](https://github.com/probe-rs/probe-rs/tree/master/target-gen#target-gen)生成

Burn algorithm files, Keil patch pack. The file name needs to correspond to yaml
Generate by[`target-gen`](https://github.com/probe-rs/probe-rs/tree/master/target-gen#target-gen)

`target-gen pack xxx.pack ./`

## config.yaml

配置文件，描述了目标芯片型号，烧录所需算法，烧录速率等

Configuration file, describing the target chip model, required algorithm for burning, burning rate, etc

```yaml
chip: HC32F4A0PGTB
pack_yaml: ./HC32F4A0-Series.yaml
speed: '16000'
base_address: '0x00000000' #just for bin file, default is 0x08000000. negligible
```
