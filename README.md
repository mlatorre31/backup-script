# Backup Script
This is a very basic Python script that allows backing up a directory and its contents, either by duplicating the whole tree, or creating a tar archive.

While usually the contents of the script would've been split into different files for a clear separation of concerns, we wanted to keep it simple and nothing is simpler that one single file.

### Requirements
Python is required for running this script. It was developed using Python 2.7.10, and as the time of writing this hadn't been tested on Python 3, but should work.

### Usage
Configure your options in the `config.yml` file and then simple execute the script:
 
```$ python backup.py```

### Configuration
The configuration is done through a simple yaml file, where each block (starting with `---`) represents a different backup configuration. Meaning you can use the same execution to backup multiple targets, with different rules for each.
You can use the supplied `config.yml` as reference and consult the docs [here](https://unravelling-technologies.github.io/backup-script).