


const regiser = async (data, updateUser) => {
  const response = await fetch('http://localhost:8000/register/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  const responseData = await response.json();
  if (responseData === "user email exists"){
    return false;
  }
  else {
    updateUser({
      id: responseData[0],
      name: responseData[1],
      email: responseData[3],
      password: responseData[2]
    });
    get_user_wines(responseData[0] , updateUser);
    // Assuming getUser() is a valid function that fetches the updated user data
    //console.log("get user -- > ", getUser());
    return true;
  }
};


const login_server = async (data, updateUser) => {
  const response = await fetch('http://localhost:8000/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    // If the response status code is not in the 200-299 range
    // Handle login failure (e.g., incorrect credentials)
    console.log("Login failed");
    return false;
  }
  const responseData = await response.json();
  updateUser({
    id: responseData.user[0], // Adjust according to the actual response structure
    name: responseData.user[1],
    email: responseData.user[3],
    password: responseData.user[2] // Be cautious about storing passwords on the client side
  });
  get_user_wines(responseData.user[0], updateUser);
  return true;
};



const get_user_wines = async (userID , updateUser) => {
  console.log("get_user_wines -- > id ", userID);
  const response = await fetch('http://localhost:8000/details/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ userID }),  

  });
  if (!response.ok) {
    // If the response status code is not in the 200-299 range
    // Handle login failure (e.g., incorrect credentials)
    console.log("Login failed");
    return false;
  }
  const responseData = await response.json();
  const transformProductsArrayToMap = (responseData) => {
    const productsMap = new Map();
    responseData.data.forEach(responseData => {
      const [id, name, date, derech_hayin, paneco, haturkey] = responseData;
      productsMap.set(id, {
        id,
        name,
        date,
        derech_hayin,
        paneco,
        haturkey
      });
    });
    
    return productsMap;
  };
    const productsObject = transformProductsArrayToMap(responseData);
    const serializedProducts = JSON.stringify(Array.from(productsObject.entries()));
    console.log("productsObject---> " , productsObject);
    updateUser({products:serializedProducts})
    return true  ;
};


const addWine = async (data, updateUser) => {
  const response = await fetch('http://localhost:8000/addwine/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
}


  export { login_server  , regiser , addWine , get_user_wines};