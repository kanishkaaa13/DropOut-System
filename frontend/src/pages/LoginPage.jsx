import { useState } from "react";
import { registerUser, loginUser } from "../api";

export default function LoginPage({ onLoggedIn, onBack }) {
  const [mode, setMode] = useState("login"); // "login" | "register"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [error, setError] = useState("");

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");
    try {
      let data;
      if (mode === "register") {
        data = await registerUser(email, password, role);
      } else {
        data = await loginUser(email, password);
      }
      localStorage.setItem("token", data.access_token);
      onLoggedIn(role);
    } catch (err) {
      console.error(err);
      setError("Authentication failed");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <button onClick={onBack} style={{ marginBottom: "1rem" }}>
        ← Back
      </button>
      <h2>{mode === "login" ? "Login" : "Register"}</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit} style={{ maxWidth: 400 }}>
        <div style={{ marginBottom: "0.75rem" }}>
          <label>Email</label>
          <input
            type="email"
            required
            value={email}
            onChange={e => setEmail(e.target.value)}
            style={{ width: "100%", padding: "0.5rem" }}
          />
        </div>
        <div style={{ marginBottom: "0.75rem" }}>
          <label>Password</label>
          <input
            type="password"
            required
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{ width: "100%", padding: "0.5rem" }}
          />
        </div>
        {mode === "register" && (
          <div style={{ marginBottom: "0.75rem" }}>
            <label>Role</label>
            <select
              value={role}
              onChange={e => setRole(e.target.value)}
              style={{ width: "100%", padding: "0.5rem" }}
            >
              <option value="student">Student</option>
              <option value="admin">Admin</option>
            </select>
          </div>
        )}
        <button type="submit" style={{ padding: "0.5rem 1rem" }}>
          {mode === "login" ? "Login" : "Register"}
        </button>
      </form>

      <p style={{ marginTop: "1rem" }}>
        {mode === "login" ? "New here?" : "Already registered?"}{" "}
        <button
          type="button"
          onClick={() => setMode(mode === "login" ? "register" : "login")}
          style={{ textDecoration: "underline", background: "none", border: "none", cursor: "pointer" }}
        >
          {mode === "login" ? "Create account" : "Login"}
        </button>
      </p>
    </div>
  );
}
