import React from 'react';

const LogoutButton = () => {
  const handleClick = () => {
    // TODO: Perform logout action here, removing the username from local storage
	fetch("http://127.0.0.1:5000/logout", {
	  method: "POST",
	  headers: {
	    "Content-Type": "application/json",
	    'Accept': 'application/json'
	  },
	  body: JSON.stringify({ logout: true })
	})
	  .then((res) => {
	    if (!res.ok) {
	      console.error('Response not OK:', res.status, res.statusText);
	      throw new Error(res.statusText);
	    }
	    return res.json();
	  })
	// removing the username from local storage
	localStorage.removeItem('username');
    // Redirect the user to the login page
	window.location.href = '/login';
  };

  return (
    <button onClick={handleClick}>Logout</button>
  );
};

export default LogoutButton;