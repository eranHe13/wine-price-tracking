import React, {   useState, useEffect }  from "react";
import { FaWineBottle , FaTrash  } from "react-icons/fa";
import {useUser} from "./user";
import {addWine , get_user_wines} from "../server"
import AddProductForm from "./add_Wine_Form";
import ProductDetails from "./product_details"

// const ProductDetails = ({ product }) => (
//   <div style={{justifyContent:"center" }}>
//     <h3>{product.name}</h3>
//     <p>דרך היין : {product.derech_hayin}</p>
//     <p>פנקו : {product.paneco}</p>
//     <p>הטורקי : {product.haturkey}</p>

//     {/* You can display more product details here */}
//   </div>
// );



function Home(props) {
  const { user , updateUser  } = useUser();
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAddProduct, setShowAddProduct] = useState(false);
  

useEffect(() => {
  if (user.products && user.products.length > 0) {
    const arr = JSON.parse(user.products);
    setProducts(arr.map(([key, obj]) => ({
      ...obj,
      key // Adding the key from the array to the object
    })));
  }
}, [user.products]);


  const handleAddProductClick = () => {
    setShowAddProduct(true);
    setSelectedProduct(null); // Deselect any selected product
  };

  
  const handleProductClick = (product) => {
    setShowAddProduct(null);
    setSelectedProduct(product);
  };

  const handleDeleteProduct = async (productId) => {
    try {
     const response = await fetch(`http://localhost:8000/remove_wine/${user.id}/${productId}`, {
  method: 'DELETE',
});

      if (!response.ok) {
        throw new Error('Failed to delete product');
      }

       // Remove the deleted product from the frontend state
    setProducts(products.filter(product => product.id !== productId));
    setSelectedProduct(null); // Deselect any selected product
  } catch (error) {
    setError("Error deleting product: " + error.message);
  }
};

  // const handleDeleteProduct = (key) => {
  //   // Update products state to filter out the deleted product
  //   setProducts(products.filter(product => product.key !== key));
  //
  //   // Optionally, add code here to also delete the product from the server or database
  // };



  if (isLoading) return <p>Loading products...</p>;
  if (error) return <p>Error fetching products: {error}</p>;

 
  return (
    <div >
    <div calss="d-block" className="header"  style={{height:"100px"}} >
      <nav class="navbar bg-body-tertiary"   style={{height:"100%" }}>
        <div class="container position-absolute top-0 start-0" style={{height:"100%" , marginLeft:"15px" , fontSize:"40px"}}>
        <FaWineBottle />
          {user.name}
        </div>
      </nav>
    </div>
    <div style={{ display: 'flex', flexDirection: 'row', height: '100vh' }}>
    <div style={{ flex: '1', overflowY: 'auto', borderRight: '1px solid #ccc' }}>
      <div class="d-flex justify-content-center"  >
    <button class="btn btn-primary" onClick={handleAddProductClick } style={{marginTop:"20px" ,width:"80%" , fontSize:"20px" }}>add new wine</button>
    </div>
    <div class="d-flex justify-content-center"  >
      <ul style={{ listStyleType: 'none', paddingLeft: "15px" , paddingTop:"15px"  , fontSize:"27px" ,  direction:"rtl"}}>
        {products.map((product) => (
          <li key={product.key} style={{ padding: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}>
          <span onClick={() => handleProductClick(product)}>{product.name}</span>
          <FaTrash onClick={() => handleDeleteProduct(product.key)} style={{ cursor: 'pointer' ,width:"17px" , height:"17px" , marginRight:"15px"}}/>
        </li>
        ))}
      </ul>
      </div>
    </div>
    <div style={{ flex: '4', padding: '20px' , alignContent:"center" }}>
    {showAddProduct ? (
          <AddProductForm user={user} updateUser={updateUser} />

        ) : selectedProduct ? (
          <ProductDetails product={selectedProduct} />
        ) : (
          <p>Select a product to view details or add a new product.</p>
        )}    </div>
  </div>
  </div>
 
  );
}

export default Home;



