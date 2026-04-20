---
created: '2024-04-20'
id: readme
synced_at: '2026-04-20T17:22:22.453892+00:00'
title: readme
type: plain-doc
version: '0.1'
---

# path-key [![Build Status](https://travis-ci.org/sindresorhus/path-key.svg?branch=master)](https://travis-ci.org/sindresorhus/path-key)

> Get the [PATH](https://en.wikipedia.org/wiki/PATH_(variable)) environment variable key cross-platform

It's usually `PATH`, but on Windows it can be any casing like `Path`...


## Install

```
$ npm install path-key
```


## Usage

```js
const pathKey = require('path-key');

const key = pathKey();
//=> 'PATH'

const PATH = process.env[key];
//=> '/usr/local/
