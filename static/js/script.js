let cvsIn = document.getElementById("inputimg");//id of canvas
let ctxIn = cvsIn.getContext('2d');
let divOut = document.getElementById("predictfruit");//id of right boxitem

let mouselbtn = false;

window.onload = function()
{

    ctxIn.fillStyle = "white";
    ctxIn.fillRect(0, 0, cvsIn.width, cvsIn.height);
    ctxIn.lineWidth = 7;
    ctxIn.lineCap = "round";

}

cvsIn.addEventListener("mousedown", function(e){

    if(e.button == 0){
        let rect = e.target.getBoundingClientRect();//e=canvas element
        let x = e.clientX - rect.left;//x's position wrt canvas (x wrt full - canvas wrt full)
        let y = e.clientY - rect.top;
        mouselbtn = true;
        ctxIn.beginPath();
        ctxIn.moveTo(x, y);
    }
    else if(e.button == 2){
        onClear();
    }
});


cvsIn.addEventListener("mouseup", function(e) {
    if(e.button == 0){
        mouselbtn = false;
        onRecognition();
    }
});
cvsIn.addEventListener("mousemove", function(e) {
    let rect = e.target.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;
    if(mouselbtn){
        ctxIn.lineTo(x, y);
        ctxIn.stroke();
    }
});
document.getElementById("clearbtn").onclick = onClear;
function onClear(){
    mouselbtn = false;
    ctxIn.fillStyle = "white";
    ctxIn.fillRect(0, 0, cvsIn.width, cvsIn.height);
    ctxIn.fillStyle = "black";
}

// post data to server for recognition
function onRecognition() {
    console.time("time");
    //Jquery
    $.ajax({
            url: './Recognition',
            type:'POST',
            data : {img : cvsIn.toDataURL("image/png").replace('data:image/png;base64,','') },
            //Replacing data:image/png;base64 in our image because its useless information
            //its send as a url in base64 format to server
        }).done(function(data) {
            showResult(JSON.parse(data))//converted json string to javascript object
            //JSON.parse() method parses a JSON string, constructing the JavaScript value or object described by the string
            //here, its creating a JS object.
            //objects in JS are similar to dictionary in Python

        }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest);
            alert("error");
        })

    console.timeEnd("time");
}


function showResult(resultJson)
{
    // resultJson has a JS object and predict_fruit is the key
    divOut.textContent = resultJson.predict_fruit;
}
