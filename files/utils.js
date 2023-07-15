function redirect(url) {
    window.location.replace(url);
}

// function getRequest(url) {
//     return new Promise((resolve, reject) => {
//     const xhr = new XMLHttpRequest();
//         xhr.open("GET", url);
//         xhr.onload = () => resolve(xhr);
//         xhr.onerror = () => reject(xhr.status);
//         xhr.send();
//     });
// }

var activeToast = "";
var toastErr = "";
var sameToastCount = 1;

function randomStr(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function say(message) {
    console.log("%c"+message, "color: #00ffa8")
}

function toast(message, infoType="default") {
    // Default -> Accent color
    // Warn -> Yellow color   
    // Success -> Green color
    // Error/Fail -> Red color
    // [!] KEEP INFOTYPE LOWERCASE

    //remove previous toast if exists
    try {
        let prevToast = document.getElementById("toast-"+activeToast);
        if (prevToast != null) {
            if (prevToast.innerHTML == message || prevToast.innerHTML == message + ` ${sameToastCount}x`) {
                sameToastCount++;
                prevToast.innerHTML = message + ` ${sameToastCount}x`;
                return;
            }
            sameToastCount = 1;
            prevToast.remove();
        }
    } catch (e) { toastErr = e; }

    //register a toast msg
    let toastId = randomStr(5)
    activeToast = toastId

    //create a toast box
    let box = document.createElement("div");
    box.innerHTML = message;
    box.className = `toast toast-${infoType}`;
    box.id = `toast-${toastId}`

    //make it work
    document.getElementById("toastspace").appendChild(box);
    console.log("%c[XELLOBLUE] Toast message shown (ID: "+toastId+")", "color: #A79FFF");
    
    setTimeout(function () {
        //delete current toast if still exists
        try {
            let prevToast = document.getElementById("toast-"+toastId);
            if (prevToast != null) {
                prevToast.remove();
                sameToastCount = 1;
            }
        } catch (e) { toastErr = e; }
    }, 5000);
    return toastId;
}
