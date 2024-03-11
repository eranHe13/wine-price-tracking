import React from 'react';

const ProductDetails = ({ product }) => {
    const img = product.product_image ? product.product_image: null;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%' }}>
      
      {/* Product Name in the Center */}
      
      <h2 class="display-1" style={{ textAlign: 'center' }}>{product.name}</h2>
      <h3 style={{ textAlign: 'center' }}>My Desire Price : {product.desire_price}</h3>
      <div style={{ display: 'flex', justifyContent: 'space-around'   }}>
        {/* Product Details on the Left */}
       
        <table class="table" style={{ padding: '0 20px', direction: 'rtl' , fontSize:"25px" }}>
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Store</th>
              <th scope="col">Price</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">1</th>
              <td>דרך היין</td>
              <td>{product.derech_hayin}</td>
            </tr>
            <tr>
              <th scope="row">2</th>
              <td>פנקו</td>
              <td>{product.paneco}</td>
            </tr>
            <tr>
              <th scope="row">3</th>
              <td>הטורקי</td>
              <td>{product.haturkey}</td>
            </tr>
            {/* Additional product details can be dynamically inserted here */}
          </tbody>
        </table>
        
        <div >

        {/* Product Image and Description on the Right */}
        <div  style={{  textAlign: 'center', padding: '0 20px' , height:"400px" }}>
          <img class="card-img-top" src={img} alt={product.name} style={{height:"400px"}} />
          <p class="card-text" >Some words about the wine</p>
          <p class="card-text"><small class="text-body-secondary">Last updated 3 mins ago</small></p>
        </div>
      </div>
      </div>
    </div>
  );
};

export default ProductDetails;

// <div style={{ flex: 1, padding: '0 20px', direction: 'rtl' }}>
//           <p>דרך היין : {product.derech_hayin}</p>
//           <p>פנקו : {product.paneco}</p>
//           <p>הטורקי : {product.haturkey}</p>
//           {/* Additional product details can go here */}
//         </div>
