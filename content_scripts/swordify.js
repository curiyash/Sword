(function() {
    /**
     * Check and set a global guard variable.
     * If this content script is injected into the same page again,
     * it will do nothing next time.
     */
    console.log("Swordifying");
    if (window.hasRun) {
      return;
    }
    window.hasRun = true;
    let images = [];
    let meta;
    /**
     * Given a URL to a beast image, remove all existing beasts, then
     * create and style an IMG node pointing to
     * that image, then insert the node into the document.
     */

     function minimize(e){
      console.log("Here1");
      let w = document.getElementsByClassName('word')[0];
      let text = document.getElementsByClassName('wordText')[0];
      let box = document.getElementsByClassName('box')[0];
      w.style.overflow = "hidden";
      w.style.width = `${text.clientWidth+this.clientWidth+64}px`;
      console.log(this.clientWidth);
      w.style.height = `${box.clientHeight+10}px`;
      w.removeChild(miniImg);
      w.appendChild(maxiImg);
    }

    function maximize(e){
      console.log("Here2");
      let w = document.getElementsByClassName('word')[0];
      w.style.overflow = "scroll";
      w.style.width = "420px";
      w.style.height = "auto";
      w.removeChild(maxiImg);
      w.appendChild(miniImg);
    }

    let timer;
    let maxiImg = document.createElement('img');
    maxiImg.onclick = maximize;
    // maxiImg.src = 'https://i.ibb.co/zs20fy4/maximize.png';
    maxiImg.src = 'https://i.ibb.co/PGkyfW7/plus.png'
    maxiImg.id = 'window';
    let miniImg = document.createElement('img');
    miniImg.id = 'window';
    miniImg.onclick = minimize;
    // miniImg.src = "https://i.ibb.co/ZHPFwFs/minimize.png";
    miniImg.src = "https://i.ibb.co/ZNsHrhQ/minus.png";

    function playAudio(){
      clearInterval(timer);
      let image = document.getElementsByClassName('audio-img')[0];
      let a = document.getElementsByClassName('src-audio')[0];
      let dur = a.duration;
      console.log(dur);
      var x = 0;
      timer = setInterval(()=>{
        if (x%2==0){
          image.classList.add('flip-horizontally');
        } else{
          image.classList.remove('flip-horizontally');
        }
        x+=1;
      }, (dur*1000)/5);
      a.play();
      a.onended = function(){
        clearInterval(timer);
      }
    }

    function changePos(e){
      if (!(this.classList.contains('active'))){
        let act = document.getElementsByClassName('active')[0];
        act.classList.remove('active');
        this.classList.add('active');
        let poSpeech = this.innerText.trim();
        let parentDiv = document.getElementsByClassName('word')[0];
        let imgDiv = document.getElementsByClassName('thumbs');
        if (imgDiv.length!==0){
          imgDiv = imgDiv[0];
          parentDiv.removeChild(imgDiv);
        } else{
          imgDiv = null;
        }
        var meanings = document.getElementsByClassName('meanings');
        if (meanings.length!==0){
          meanings[0].remove();
        }
        let meaningsDiv = document.createElement('div');
        meaningsDiv.className = 'meanings';

        let word = document.getElementsByClassName('wordText')[0].innerText;

        let syn = meta[` ${poSpeech}`][1][' Synonyms'];
        let ant = meta[` ${poSpeech}`][1][' Antonyms'];
        let rel = meta[` ${poSpeech}`][1][' Related terms'];
        const url = `http://localhost:8000/pos/${word}/${poSpeech}/${syn}/${ant}/${rel}/`;
        caller(url, parentDiv, meaningsDiv, imgDiv);
        console.log("Here");
      }

      async function update(url, meaningsDiv){
        console.log("Inside");
        fetch(url)
        .then(response => response.json())
        .then(data => {
          for (const [key, value] of Object.entries(data)){
            if (!isNaN(key)){
              console.log(`${key} ${value}`);
              let newP = document.createElement('p');
              newP.style.overflow = "hidden";
              newP.className = "para-word"
              newP.innerText = `${key}. ${value.meaning}`;
              meaningsDiv.appendChild(newP);
            }
          }
        }
        );
      }

      async function caller(url, parentDiv, meaningsDiv, imgDiv){
        await update(url, meaningsDiv);
        parentDiv.appendChild(meaningsDiv);
        if (imgDiv!==null){
          parentDiv.appendChild(imgDiv);
        }
      }
    }

    function insertMeaning() {
      console.log("Inside");
      let poses = [];
      let selection = window.getSelection();
      let word = selection.toString()
    //   let rect = selection.getRangeAt(0).getBoundingClientRect();
      var r=window.getSelection().getRangeAt(0).getBoundingClientRect();
      var relative=document.body.parentNode.getBoundingClientRect();
      removeExistingWords();
      let newDiv = document.createElement("div");      

      // let newP = document.createElement("p");
      newDiv.className = "word";
      newDiv.classList.add('unstick');
      // newP.style.inlineSize = "210px";
      // newP.style.overflow = "hidden";
      // newP.className = "para-word"
      // newDiv.style.position = "absolute";
      newDiv.style.top = `calc(${r.top}px - ${relative.top}px - 72px)`;
      newDiv.style.left = `calc(${r.left}px`;
      let newH = document.createElement('div');
      let newHA = document.createElement('a');
      newH.appendChild(newHA);
      newSpan = document.createElement('span');
      newSpan.className = "pos";
      newH.className = 'wordText';
      newDiv.appendChild(miniImg);

      let imgDiv = document.createElement('div');
      imgDiv.className = 'thumbs';

      let posDiv = document.createElement('div');
      posDiv.id = "speech";

      let meaningsDiv = document.createElement('div');
      meaningsDiv.classList.add('meanings');

      let box = document.createElement('div');
      box.className = 'box';

      newAudio = document.createElement('img');
      newAudio.className  = 'audio-img';
      newAudio.src = 'https://i.ibb.co/xs4B7HW/sound-waves-1.png';
      newAudioA = document.createElement('audio');
      newAudioA.className = 'src-audio';
      newSource = document.createElement('source');
      const url = `http://localhost:8000/wiki/${word.toLowerCase().trim()}/`;
      if (word===""){
            box.classList.remove("box");
            newDiv.removeChild(miniImg);
            box.classList.add("not-found");
            box.style.paddingRight = "10px";
            box.style.paddingLeft = "10px";
            box.innerText = "No word is selected. Highlight a word to find its meaning";
            box.style.paddingRight = "10px";
            box.style.paddingLeft = "10px";
            newDiv.style.top = `${window.pageYOffset+window.innerHeight/2}px`;
            newDiv.style.left = `${window.pageXOffset+window.innerWidth/2}px`;
            newDiv.appendChild(box);
            document.body.appendChild(newDiv);
            dragElement(document.getElementsByClassName("not-found")[0]);
      return;
      }
      async function getJSON(){
      fetch(url)
        .then(response => response.json())
        .then(data => {
          images = []
          if (data===null){
            newDiv.removeChild(box);
            // newDiv.appendChild(newSpan);
            newDiv.removeChild(posDiv);
            newDiv.removeChild(imgDiv);
            newDiv.removeChild(miniImg);
            box.classList.remove("box");
            box.style.paddingRight = "10px";
            box.style.paddingLeft = "10px";
            box.innerText = "Sorry, not able to find meaning for it. ";
            box.style.cursor = "move";
            box.style.paddingRight = "10px";
            box.style.paddingLeft = "10px";
            let a = document.createElement('a');
            a.href = `https://www.google.com/search?q=${word.toLowerCase().trim()} meaning`;
            a.innerText = "How about Googling it?"
            box.appendChild(a);
            newDiv.appendChild(box);
            return;
          } else{
            for (const [key, value] of Object.entries(data)){
              // console.log(value);
              if (!isNaN(key)){
                console.log(`${key} ${value}`);
                let newP = document.createElement('p');
                newP.style.overflow = "hidden";
                newP.className = "para-word"
                newP.innerText = `${key}. ${value.meaning}`;
                meaningsDiv.appendChild(newP);
              }else if (key==="img_tags"){
                value.forEach(function (item){
                  let newImg = document.createElement('img');
                  newImg.src = item;
                  newImg.className = "thumbimage";
                  images.push(newImg);
                })
              }else if (key==="word"){
                newHA.innerText = value;
                newHA.href = `https://en.wiktionary.org/wiki/${value}`
              }else if (key==="pos"){
                let sp = document.getElementsByClassName('pos');
                console.log(sp);
                console.log(value);
                for (const s of sp){
                  if (value==s.innerText){
                    s.classList.add("active");
                  }
                }
              }else if (key==="audio"){
                if (value!=null){
                  newAudio.onclick = playAudio;
                  newSource.src = `https:${value}`;
                  newSource.type = 'audio/ogg';
                }
                newAudioA.appendChild(newSource);
                newAudioA.onClick = playAudio;
                newAudio.appendChild(newAudioA);
              }else if (key==="synonyms"){
                value.forEach(function (synonym){
                  console.log(synonym);
                })
              } else if (key==="meta"){
                  meta = value;
                  for (const [key, val] of Object.entries(value)){
                    if (key!=='meta_info'){
                      if (val[0]===true){
                        let otherPos = document.createElement('span');
                        otherPos.className = "pos";
                        otherPos.innerText = key.trim();
                        otherPos.onclick = changePos;
                        posDiv.appendChild(otherPos);
                      }
                    }
                  }
              }
            }
            images.forEach(function(image){
              imgDiv.appendChild(image);
            })
          }
        })
      }

      async function caller(){
        await getJSON();
        if (images.length!==0){
          console.log(images.length);
          console.log("Not empty");
            console.log(images[0]);
          }
      }
      if (word!==''){
        box.appendChild(newH);
        box.appendChild(newAudio);
        newDiv.appendChild(box);
        // newDiv.appendChild(newSpan);
        newDiv.appendChild(posDiv);
        newDiv.appendChild(meaningsDiv);
        console.log(poses);
        caller();
        newDiv.appendChild(imgDiv);
      }

    // newP.innerText = "Hello there";
    document.body.appendChild(newDiv);
      
      // Make the DIV element draggable:
      dragElement(document.getElementsByClassName("box")[0]);
    }
    
    /**
     * Remove every beast from the page.
     */
    function removeExistingWords() {
      let existingBeasts = document.querySelectorAll(".word");
      for (let beast of existingBeasts) {
        beast.remove();
      }
    }

    function hide(){
      let popup = document.getElementsByClassName('word')[0];
      popup.style.display = "none";
    }

    function show(){
      let popup = document.getElementsByClassName('word')[0];
      popup.style.display = "";
    }
    function stickify(){
      let w = document.getElementsByClassName('word');
      if (w.length!==0){
        w = w[0];
        w.style.top = "100px";
        w.style.right = "0px";
        w.classList.toggle('stick');
        w.classList.toggle('unstick');
        if (w.classList.contains('unstick')){
          w.style.top = `${window.pageYOffset+100}px`;
          w.style.right = `${window.pageXOffset}px`;
        }
      }
    }
  
    /**
     * Listen for messages from the background script.
     * Call "insertBeast()" or "removeExistingBeasts()".
     */
    browser.runtime.onMessage.addListener((message) => {
      if (message.command === "swordify") {
        insertMeaning();
      } else if (message.command === "hide"){
        hide();
      } else if (message.command === "show"){
        show();
      } else if (message.command === "stick"){
        stickify();
      }
    });
  
    function dragElement(elmnt) {
      var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
      var movee = document.getElementsByClassName('word')[0];
      elmnt.onmousedown = dragMouseDown;
    //   if (document.getElementById(elmnt.id + "header")) {
        // if present, the header is where you move the DIV from:
        // document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
    //   } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        // elmnt.onmousedown = dragMouseDown;
    //   }
    
      function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
      }
    
      function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        movee.style.top = (movee.offsetTop - pos2) + "px";
        movee.style.left = (movee.offsetLeft - pos1) + "px";
      }
    
      function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
      }
    }
  
  })();
