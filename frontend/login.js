// src/Login.js
import React from "react";
import { auth, provider } from "./firebase";

const Login = () => {
  const signInWithGoogle = () => {
    auth.signInWithPopup(provider)
      .then((result) => {
        console.log("Logged in:", result.user);
      })
      .catch((error) => {
        console.error("Error during sign in:", error);
      });
  };

  return (
    <div className="login-container">
      <h1>REAL TIME DROWSINESS DETECTOR</h1>
      <button onClick={signInWithGoogle}>Login with Google</button>
    </div>
  );
};

export default Login;
