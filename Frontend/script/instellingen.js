"use script";
const IP = window.location.hostname + ':5000';
const socket = io.connect(IP)


const listenToUI = function () {
    const knoppen = document.querySelectorAll(".js-aan");
    for (const knop of knoppen) {
        knop.addEventListener("click", function () {
            console.log("ik klikte op aan")
            socket.emit("F2B_alle_aan")
        });
    }
    const knoppen_uit = document.querySelectorAll(".js-uit");
    for (const knop of knoppen_uit) {
        knop.addEventListener("click", function () {
            console.log("ik klikte op uit")
            socket.emit("F2B_alle_uit")
        });
    }
};

const listenToSocket = function () {
    socket.on("connect", function () {
        console.info("verbonden met socket webserver");
    });
}

//#region ***********  Data Access ***********
// get_______
const get_ip = function () {
    handleData(`http://${IP}/IP`, show_ip, 'GET');
};
//#endregion

const show_ip = function (jsonObject) {
    console.log(jsonObject)
    let html_string = "";
    console.log("IP ontvangen");
    html_string += `IP adres = ${jsonObject}`
    html_ip.innerHTML = html_string;

}

document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    html_ip = document.querySelector('.js-ip');
    get_ip();
    listenToUI();
    listenToSocket();

});
