function makeGetRequest(path) { 
    axios.get(path).then( 
        (response) => { 
            var result = response.data; 
            console.log(result); 
        }, 
        (error) => { 
            console.log(error); 
        } 
    ); 
} 
makeGetRequest('http://localhost:5000/api'); 