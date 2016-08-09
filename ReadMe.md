# Photos date fixer

Updates the exif information in JPEG files to make sure that there is a Date.
If the file has no date information, then it gets it from the extended exif information or the file folders in the path.

**The updates the original file. Please to a backup of your files before!** 

# Setup
```
	pip install -r requirements
```

# Execute
```
	python fix_dates.py ~/photos/
```