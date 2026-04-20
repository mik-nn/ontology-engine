---
created: '2024-04-20'
id: README
synced_at: '2026-04-20T17:22:22.257869+00:00'
title: README
type: plain-doc
version: '0.1'
---

# which

Like the unix `which` utility.

Finds the first instance of a specified executable in the PATH
environment variable.  Does not cache the results, so `hash -r` is not
needed when the PATH changes.

## USAGE

```javascript
var which = require('which')

// async usage
which('node', function (er, resolvedPath) {
  // er is returned if no "node" is found on the PATH
  // if it is found, then the absolute path to the exec is returned
})

// or promise
which('node').then(resolvedPath => { ... 
