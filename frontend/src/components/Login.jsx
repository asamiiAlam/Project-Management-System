import { useState } from "react";
import "./Login.css";

function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [showPassword, setShowpassword] = useState(false);

  const handleLogin = async () => {
    setError("");
    setSuccess(false);

    if (username.trim() === "") {
      setError("Udername can not be blank");
      return;
    }

    if (email.trim() === "" || !email.includes("@")) {
      setError("Please enter a valid email");
      return;
    }

    if (password.trim() === "") {
      setError("You have to write pass");
      return;
    }

    try {
      const response = await fetch(
        "https://project-management-system-ekr7.onrender.com/api/login/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: username.trim(),
            password: password,
          }),
        },
      );

      const data = await response.json();
      console.log(data);

      if (!response.ok) {
        setError(data.detail || "Login failed. check your credentials");
        return;
      }
      if (!data.access || !data.refresh) {
        setError("Login failed: Tokens not received.");
        return;
      }

      localStorage.setItem("accessToken", data.access);
      localStorage.setItem("refreshToken", data.refresh);
      setSuccess(true);
      onLoginSuccess();
    } catch {
      setError("Cannot connect to the server. Please try again");
    }
  };

  return (
    <div className="login-container">
      <h1>Login Page</h1>
      <p>Welcome:Please login to continue</p>

      <label htmlFor="username">Username</label>
      <input
        type="text"
        id="username"
        placeholder="Enter your username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <label htmlFor="email">Email</label>
      <input
        type="email"
        id="email"
        placeholder="Enter you email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      ></input>

      <label htmlFor="password">Password</label>
      <input
        type={showPassword ? "text" : "password"}
        id="password"
        placeholder="Enter your password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      ></input>

      <button type="button" onClick={() => setShowpassword(!showPassword)}>
        {showPassword ? "Hide" : "Show"}
      </button>

      <button type="button" onClick={handleLogin}>
        Login
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>Login Successfull</p>}
    </div>
  );
}
export default Login;
