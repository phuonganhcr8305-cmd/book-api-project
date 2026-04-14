import React from "react";

function Register() {
  return (
    <div>
      <h1>Sign Up</h1>

      <form>
        <input type="text" placeholder="Username" /><br /><br />
        <input type="text" placeholder="First Name" /><br /><br />
        <input type="text" placeholder="Last Name" /><br /><br />
        <input type="email" placeholder="Email" /><br /><br />
        <input type="password" placeholder="Password" /><br /><br />

        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
