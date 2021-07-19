getData(); 

        async function getData() {
            const response = await fetch('test.csv');
            const data = await response.text(); 
            console.log(data); 

            const rows = data.split('\n').slice(1);
            rows.forEach(elt => {
                const row = elt.split(',');
                const year = row[0];
                const temp = row[1];

                console.log(year, temp);

            });
            console.log(rows);

        }


/*var headers = {
    'Accept':'application/json'
   
  };
   
  $.ajax({
    url: 'https://api.carbonintensity.org.uk/intensity',
    method: 'get',
   
    headers: headers,
    success: function(data) {
      console.log(JSON.stringify(data));
    }
  })
  */


var ourRequest = new XMLHttpRequest(); 

var baseUrl = "https://ghibliapi.herokuapp.com"

ourRequest.open('GET', baseUrl); 
ourRequest.onload = function() {
    var ourData = JSON.parse(ourRequest.responseText); 
    console.log(ourData[0]);
};
ourRequest.send();

async function start() {
    const response = await fetch(baseUrl)
    const data = await response.json()
    createTitle(data.message)
}

start()

function createTitle(title){
    document.getElementById("breed").innerHTML = `
    <select onchange = "loadByBreed(this.value)"> 
        <option> Choose a dog breed </option>
        ${Object.keys(title).map(function (title){
            return `<option> ${breed} </option>`
        }).join('')}
        </select>
    `
}

async function loadByBreed(breed) {
    if (breed != "Choose a dog") {
        const response = await fetch(`baseUrl`)
        const data = await response.json()
        console.log(data)
    }
}

