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


