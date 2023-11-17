list = [];
    // show hidden box and buttons
    function show_keys() {
        var box = document.getElementById('hiden');
        if (box.style.display == 'none') {
            document.getElementById('start').style.display = 'none';
            box.style.display = 'block';
            document.getElementById('player_button').style.display = 'block';
            document.getElementById('order_button').style.display = 'block';
        }
}
    
    // show first player
    function show_player () {
        text = document.getElementById('player_text')
        button = document.getElementById('player_button')
        if (text.style.display == 'none') {
            text.style.display = 'block';
            button.style.fontSize = '1.2rem';
            button.style.padding = '0.5rem 1rem';
        }
}
    
    // show random order
    function show_order () {
        text = document.getElementById('order_text')
        button = document.getElementById('order_button')
        if (text.style.display == 'none') {
            text.style.display = 'block';
            button.style.fontSize = '1.2rem';
            button.style.padding = '0.5rem 1rem';
        }
    }

    // Start displaying when button is clicked
    function keys() {
        // disable button
        document.getElementById("start").disabled = true
        all = [];
        document.onkeypress = function(evt) {
            // find out and remember what letter is pressed
            evt = evt || window.event;
            var charCode = evt.keyCode || evt.which;
            var charStr = String.fromCharCode(charCode);
            // check if key is alphabetical or numerical
            var letterNumber = /^[\p{L}\p{N}]*$/u;
            if(charStr.match(letterNumber))
            {
                all.push(charStr);

                // display letter in a box
                var boxWidth = document.getElementById("box").scrollWidth;
                var boxHeight = document.getElementById("box").scrollHeight;
                var elem = document.createElement("div");
                elem.textContent = charStr;
                // random color of letters
                elem.style.color = "#" + Math.floor(Math.random()*16777215).toString(16);
                // else
                elem.style.position = "absolute";
                elem.style.left = ((Math.round(Math.random() * boxWidth)) * 80 / boxWidth) + "%";
                elem.style.top = ((Math.round(Math.random() * boxHeight)) * 79 / boxHeight - 5) + "%";
                elem.style.backgroundColor = "transparent";
                elem.style.fontSize = '40px';
                document.getElementById("box").appendChild(elem);
            }
        }
        list = all;
    }

    // Choose a first player
    function player() {
        document.getElementById("player").innerHTML = list[Math.floor(Math.random() * list.length)];
        document.getElementById("player").style.backgroundColor = "transparent";
    }
    
    // Make a random order
    function order() {
        let random_list = list
    .map(value => ({ value, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(({ value }) => value)
    document.getElementById("order").innerHTML = random_list.join(" ");
    document.getElementById("order").style.backgroundColor = "transparent";
    }