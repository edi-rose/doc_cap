# Documentation-Capture
Small project to automatically generate a PDF version of our strategyblocks documentation.

# Requirements / Set up 
Bot requires the user to download the latest geckodriver and to update the method getDriver with the path to the driver. 
Bot requires python3 and has only been tested on MacOs

# Current State
Bot currently can produce a PDF containing all the documentation on the live site.
Bot is dynamic and will update automatically when new pages are added / removed.
This is based on the links available on the main menu of the documentation. 

# Next Steps
PDF needs an added page which can act as an index.
Pages also need to be ordered coherantly, currently done alphabetical. 
Ideally, text would be selectable.
The Risk Management Page acts unexpectadly and needs updating on the live site to be compatatible with the bot. 
