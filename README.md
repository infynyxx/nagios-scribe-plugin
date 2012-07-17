# Nagios Scribe Plugin

## Overview

A simple Nagios check script to monitor Scribe service(s). This script is based on [nagios-plugin-mongodb](https://github.com/mzupan/nagios-plugin-mongodb) and `scribe_cat` [utility](https://github.com/facebook/scribe/blob/master/examples/scribe_cat) that comes with [Scribe](https://github.com/facebook/scribe).

## Usage

### Using in .cfg file

```
define command {
    command_name    check_scribe
    command_line    $USER1$/check_scribe.py -H $HOSTADDRESS$
}
```

### Using from command line

```
./check_scribe.py --host <127.0.0.1> --port <1463> --category <category_name> --message "Hello world"
```
