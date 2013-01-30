scripts
=======

Miscellaneous scripts

export-defect-handler.py
------------------------
This is an example of how to export defects from CoverityConnect to an
external bug tracking system.  This example just generates an arbitrary
id for the external defect and updates the issue with that external
reference.  A real implementation would interact with a real bug tracking
system and actually generate a new record.

sample-exported.xml
-------------------
This file contains sample data that might be passed to this script by
CoverityConnect.  The data was actually exported by v6.5.1.

export-defect-handler.bat
-------------------------
By placing this file in your <CoverityConnect_INSTALL_DIR>/bin directory,
you tell CoverityConnect to run this script when somebody clicks the "Export"
button from the web interface.  That button will not exist until this file
is placed in the correct location.  On *nix systems, you'll want something
similar that uses an appropriate shell syntax.
