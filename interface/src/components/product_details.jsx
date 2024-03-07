import React from 'react';

const ProductDetails = ({ product }) => {
    const img = "https:\\winest.store\\cdn\\shop\\products\\Winest___13.11.220612_700x.png"
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%' }}>
      {/* Product Name in the Center */}
      <h3 style={{ textAlign: 'center' }}>{product.name}</h3>

      <div style={{ display: 'flex', justifyContent: 'space-around', width: '100%', alignItems: 'center' }}>
        {/* Product Details on the Left */}
        <div style={{ flex: 1, padding: '0 20px', direction: 'rtl' }}>
          <p>דרך היין : {product.derech_hayin}</p>
          <p>פנקו : {product.paneco}</p>
          <p>הטורקי : {product.haturkey}</p>
          {/* Additional product details can go here */}
        </div>

        {/* Product Image and Description on the Right */}
        <div style={{ flex: 1, textAlign: 'center', padding: '0 20px' }}>
          <img src={img} alt={product.name} style={{ maxWidth: '100%', maxHeight: '200px' }} />
          <p>Some words about the wine</p>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
