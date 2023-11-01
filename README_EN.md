# probe-rs-GUI

[[中文](./README.md)] [English]

## First of all, thanks for the following project

[probe-rs](https://github.com/probe-rs/probe-rs)：An open-source MCU debugging and download project that basically supports all chips

[pygubu](https://github.com/alejandroautalan/pygubu)：An open-source and user-friendly GUI draw project that supports real-time browsing interface

## Introduction

This project is a GUI designed based on tkinter, pygubu, and probe-rs, which can directly download firmware through DAP-LINK, stlink, and jlink. Users only need to provide the package of the chip to download hex, elf, and bin files.

## Instructions for use

### Download

1. Select Download File
2. Select chip configuration file
3. Download

### Erase

1. Select chip configuration file
2. Erase chip

PS: Currently, only full chip erase is supported
