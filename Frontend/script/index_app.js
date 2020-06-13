"use script";
const IP = window.location.hostname + ':5000';
const socket = io.connect(IP)


const listenToUI = function () {
  const knoppen = document.querySelectorAll(".js-aan");
  for (const knop of knoppen) {
    knop.addEventListener("click", function () {
      console.log("ik klikte op aan")
    });
  }
};




//#region ***********  Callback - HTML Generation (After select) ***********
// show________
const showCO_his = function (jsonCO) {
  var data = [];
  var labelsCO = [];
  //console.log(jsonVochtigheid);
  for (let i of jsonCO) {
    data.push(i.SensorWaarde);
  }
  for (let i of jsonCO) {
    labelsCO.push(i.Datum);
  }
  //console.log(labelsCO);
  //console.log(data);
  var ctx = document.getElementById('myChart4').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labelsCO.reverse(),
      datasets: [{
        label: 'Koolstofmonoxide %',
        data: data.reverse(),
        backgroundColor: [
          'rgba(17, 29, 102, 0.2)',
        ],
        borderColor: [
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            suggestedMin: 0,
            suggestedMax: 40
          }
        }]
      }
    }
  });
}

const showWatertank_his = function (jsonWatertank) {
  var data = [];
  var labelsWater = [];
  //console.log(jsonVochtigheid);
  for (let i of jsonWatertank) {
    data.push(i.SensorWaarde);
  }
  for (let i of jsonWatertank) {
    labelsWater.push(i.Datum);
  }
  console.log(labelsWater);
  console.log(data);
  var ctx = document.getElementById('myChart3').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labelsWater.reverse(),
      datasets: [{
        label: 'Watertank %',
        data: data.reverse(),
        backgroundColor: [
          'rgba(17, 29, 102, 0.2)',
        ],
        borderColor: [
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            suggestedMin: 0,
            suggestedMax: 100
          }

        }]
      }
    }
  });
}

const showVochtigheid_his = function (jsonVochtigheid) {
  var data = [];
  var labelsVocht = [];
  //console.log(jsonVochtigheid);
  for (let i of jsonVochtigheid) {
    data.push(i.SensorWaarde);
  }
  for (let i of jsonVochtigheid) {
    labelsVocht.push(i.Datum);
  }
  console.log(labelsVocht);
  console.log(data);
  var ctx = document.getElementById('myChart2').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labelsVocht.reverse(),
      datasets: [{
        label: 'Vochtigheid %',
        data: data.reverse(),
        backgroundColor: [
          'rgba(17, 29, 102, 0.2)',
        ],
        borderColor: [
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            suggestedMin: 0,
            suggestedMax: 70
          }

        }]
      }
    }
  });
}

const showTemperatuur_his = function (jsonTemperatuur) {
  var data = [];
  var labelsTemp = [];
  //console.log(jsonTemperatuur);
  for (let i of jsonTemperatuur) {
    data.push(i.SensorWaarde);
  }
  for (let i of jsonTemperatuur) {
    labelsTemp.push(i.Datum);
  }
  console.log(labelsTemp);
  console.log(data);
  var ctx = document.getElementById('myChart').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labelsTemp.reverse(),
      datasets: [{
        label: 'temperatuur °C',
        data: data.reverse(),
        backgroundColor: [
          'rgba(17, 29, 102, 0.2)',
        ],
        borderColor: [
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
          'rgba(17, 29, 102,1)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            suggestedMin: 0,
            suggestedMax: 50
          }

        }]
      }
    }
  });
};
//#endregion


const listenToSocket = function () {
  socket.on("connect", function () {
    console.info("verbonden met socket webserver");
  });

  socket.on("B2F_temperatuur", function (jsonObject) {
    let html_string = "";
    console.log("Temperatuur Ontvangen.");
    console.log(jsonObject.temperatuur);
    html_string += `${jsonObject.temperatuur} °C  `
    html_temperatuur.innerHTML = html_string;
  })
  socket.on("B2F_humidity", function (jsonObject) {
    let html_string = "";
    console.log("humidity Ontvangen.");
    console.log(jsonObject.humidity);
    html_string += `${jsonObject.humidity} %`;
    html_humidity.innerHTML = html_string;
  })
  socket.on("B2F_waterniveau", function (jsonObject) {
    let html_string = ""
    console.log("WaterLevel ontvangen");
    console.log(jsonObject.waterniveau);
    html_string += `${jsonObject.waterniveau} %`;
    html_water.innerHTML = html_string;
  })
  socket.on("B2F_Co_hoeveelheid", function (jsonObject) {
    let html_string = "";
    console.log("Co ontvangen");
    console.log(jsonObject.Co);
    html_string += `${jsonObject.Co} %`;
    html_co.innerHTML = html_string;
  })
  socket.on("B2F_historiek_temp", function (jsonObject) {
    console.log("ontvangen")
    console.log(jsonObject);
  })
};

//#region ***********  Data Access ***********
// get_______
const getTemperatuur_historiek = function () {
  handleData(`http://${IP}/temperatuur`, showTemperatuur_his, 'GET');
};
const getVochtigheid_historiek = function () {
  handleData(`http://${IP}/Vochtigheid`, showVochtigheid_his, 'GET');
}
const getWatertank_historiek = function () {
  handleData(`http://${IP}/Watertank`, showWatertank_his, 'GET');
}
const getCO_historiek = function () {
  handleData(`http://${IP}/CO`, showCO_his, 'GET');
}
//#endregion

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  getTemperatuur_historiek();
  getVochtigheid_historiek();
  getWatertank_historiek();
  getCO_historiek();
  html_temperatuur = document.querySelector('.js-temperatuur');
  html_humidity = document.querySelector('.js-humidity');
  html_water = document.querySelector('.js-water');
  html_co = document.querySelector('.js-co');
  html_stand = document.querySelector('.js-stand');
  listenToSocket();
  listenToUI();

  setInterval(getTemperatuur_historiek, 600000);
  setInterval(getVochtigheid_historiek, 600000);
  setInterval(getWatertank_historiek, 600000);
  setInterval(getCO_historiek, 600000);
});
