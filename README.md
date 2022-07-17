# Sword
Add-on for Firefox to get the meaning of a highlighted word on a page

# Getting Started
1) Get Mozilla Firefox!
2) Now, type _about:debugging_ in the search bar and click on This Firefox
3) Click on Load Temporary Addon and select the manifest.json file in this folder
4) That integrates the extension with the browser
5) Now, start the backend by navigating to its folder and entering _uvicorn fetch:app --reload_
6) Wait until you get _Application setup is complete_ message
7) Head on to the browser and navigate to any page of your liking
8) Click on the blue dictionary type icon
9) Highlight __a__ word by selecting it using the cursor and click on Meaning
10) You'll soon be greeted by a black colored box ready with your meanings (and possibly images!)
