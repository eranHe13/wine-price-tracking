import React, { useState } from 'react';
import {addWine , get_user_wines} from "../server"

// Define the AddProductForm component as a function
const AddProductForm = ({ user, updateUser }) => {
  const [name, setName] = useState('');
  const [desired_price, setPrice] = useState('');
  const [error, setError] = useState('');

  const submitHandler = async (event) => {
    event.preventDefault();
    setError(''); // Clear any existing error messages

    if (!name.trim()) {
      setError('Please enter a wine name.');
      return;
    } else if (!desired_price || isNaN(desired_price) || parseFloat(desired_price) <= 0) {
      setError('Please enter a valid positive price.');
      return;
    }

    try {
      await addWine({ "user_id": user.id, "wine_name": name, "price": desired_price }, updateUser);
      get_user_wines(user.id, updateUser);
      
    } catch (error) {
      setError('An error occurred while saving the product.');
      
    }
  };

  return (
    <form onSubmit={submitHandler}>
      {error && <div style={{ color: 'red', paddingBottom: '10px' }}>{error}</div>}
      <div style={{ paddingBottom: "10px", width: "350px" }}>
        <label className="form-label" style={{ fontSize: "20px" }}>Wine Name</label>
        <input className="form-control" type="text" value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <div style={{ paddingBottom: "10px", width: "150px" }}>
        <label className="form-label" style={{ fontSize: "20px" }}>Desired Price</label>
        <input className="form-control" type="text" value={desired_price} onChange={(e) => setPrice(e.target.value)} />
      </div>
      <button className="btn btn-primary" type="submit">Save Product</button>
    </form>
  );
};

export default AddProductForm;
