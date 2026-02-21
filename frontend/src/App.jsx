import { useState } from "react";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import StudentDashboard from "./pages/StudentDashboard";

function App() {
  const [screen, setScreen] = useState("home"); // "home" | "login" | "student"
  const [role, setRole] = useState(null);

  const handleLoggedIn = userRole => {
    setRole(userRole);
    if (userRole === "admin") {
      // later you can route to AdminDashboard
      setScreen("student"); // placeholder
    } else {
      setScreen("student");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setRole(null);
    setScreen("home");
  };

  if (screen === "login") {
    return (
      <LoginPage
        onLoggedIn={handleLoggedIn}
        onBack={() => setScreen("home")}
      />
    );
  }

  if (screen === "student") {
    return <StudentDashboard onLogout={handleLogout} />;
  }

  return <HomePage onLoginClick={() => setScreen("login")} />;
}

export default App;
