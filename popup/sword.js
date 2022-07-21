/**
 * CSS to hide everything on the page,
 * except for elements that have the "beastify-image" class.
 */
 const hidePage = `.word {
    padding-top: 5px;
    padding-bottom: 5px;
    background-color: black;
    color: white;
    width: 420px;
    max-height: 420px;
    overflow: scroll;
  }
  .para-word {
    padding-left: 21px;
    padding-right: 21px;
    font-size: medium;
  }
  .thumbimage {
    width: 142px;
  }
  .wordText {
    padding-left: 21px;
    padding-right: 10px;
    font-size: 28px;
    color: white;
  }
  .pos {
    font-size: 10px;
    padding-left: 21px;
  }
  .flip-horizontally {
    transform: scaleX(-1);
  }
  .audio-img{
    width: 50px;
    cursor: pointer;
  }
  .box {
    display: flex;
    align-items: center;
    margin-top: 10px;
    cursor: move;
  }
  #window{
    position: absolute;
    width: 36px;
    top: 10px;
    right: 10px;
  }
  .active {
    text-decoration: underline;
  }
  .stick {
    position: fixed;
  }
  .unstick {
    position: absolute;
  }
  `;

/**
* Listen for clicks on the buttons, and send the appropriate message to
* the content script in the page.
*/

function listenForClicks() {
  console.log("I'm Here");
document.addEventListener("click", (e) => {
/**
* Insert the page-hiding CSS into the active tab,
* then get the beast URL and
* send a "beastify" message to the content script in the active tab.
*/

function swordify(tabs) {
    browser.tabs.insertCSS({code: hidePage}).then(() => {
        browser.tabs.sendMessage(tabs[0].id, {
        command: "swordify"
    });
    });
}

function hidefy(tabs) {
    browser.tabs.sendMessage(tabs[0].id, {
    command: "hide"
  });
}

function showify(tabs) {
    browser.tabs.sendMessage(tabs[0].id, {
    command: "show"
});
}

function stickify(tabs) {
  browser.tabs.sendMessage(tabs[0].id, {
  command: "stick"
});
}

/**
* Just log the error to the console.
*/
function reportError(error) {
console.error(`Could not swordify: ${error}`);
}

/**
* Get the active tab,
* then call "beastify()" or "reset()" as appropriate.
*/
console.log(e.target.classList);
if (e.target.classList.contains("sword")) {
browser.tabs.query({active: true, currentWindow: true})
.then(swordify)
.catch(reportError);
} else if (e.target.classList.contains("disappear")) {
  browser.tabs.query({active: true, currentWindow: true})
  .then(hidefy)
  .catch(reportError);
  } else if (e.target.classList.contains("show")) {
    browser.tabs.query({active: true, currentWindow: true})
    .then(showify)
    .catch(reportError);
    } else if (e.target.classList.contains("stick")) {
      browser.tabs.query({active: true, currentWindow: true})
      .then(stickify)
      .catch(reportError);
      }
});
}

/**
* There was an error executing the script.
* Display the popup's error message, and hide the normal UI.
*/
function reportExecuteScriptError(error) {
console.log("Here");
document.querySelector("#popup-content").classList.add("hidden");
document.querySelector("#error-content").classList.remove("hidden");
console.error(`Failed to execute beastify content script: ${error.message}`);
}

/**
* When the popup loads, inject a content script into the active tab,
* and add a click handler.
* If we couldn't inject the script, handle the error.
*/
browser.tabs.executeScript({file: "/content_scripts/swordify.js"})
.then(listenForClicks)
.catch(reportExecuteScriptError);
