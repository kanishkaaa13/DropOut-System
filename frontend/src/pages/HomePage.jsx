export default function HomePage({ onLoginClick }) {
  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <header style={{ marginBottom: "2rem" }}>
        <h1>AI-based Dropout Prediction & Counseling System</h1>
        <p style={{ maxWidth: 600 }}>
          Track student attendance, assessments and risk level in one place.
          Get early alerts and actionable counseling for at-risk learners.
        </p>
        <button onClick={onLoginClick} style={{ padding: "0.5rem 1rem" }}>
          Login
        </button>
      </header>

      <section style={{ display: "flex", gap: "2rem", flexWrap: "wrap" }}>
        <div style={{ border: "1px solid #ddd", padding: "1rem", flex: "1 1 250px" }}>
          <h3>Unified Dashboard</h3>
          <p>See attendance, test scores, and dropout risk in a single interface.</p>
        </div>
        <div style={{ border: "1px solid #ddd", padding: "1rem", flex: "1 1 250px" }}>
          <h3>Early Alerts</h3>
          <p>Color-coded risk thresholds highlight learners who need urgent help.</p>
        </div>
        <div style={{ border: "1px solid #ddd", padding: "1rem", flex: "1 1 250px" }}>
          <h3>Counseling Chatbot</h3>
          <p>Students receive personalized guidance on study habits, stress and planning.</p>
        </div>
      </section>
    </div>
  );
}
