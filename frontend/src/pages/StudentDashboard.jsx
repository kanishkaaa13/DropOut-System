import { useState } from "react";
import { predictOutcome, askCounselor } from "../api";

export default function StudentDashboard({ onLogout }) {
  const [form, setForm] = useState({
    curricular_units_1st_sem_approved: 0,
    curricular_units_1st_sem_grade: 0,
    curricular_units_2nd_sem_approved: 0,
    curricular_units_2nd_sem_grade: 0,
    admission_grade: 120,
    age_at_enrollment: 18,
  });
  const [prediction, setPrediction] = useState(null);
  const [context, setContext] = useState("");
  const [chatReply, setChatReply] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = e => {
    const { name, value } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: Number(value),
    }));
  };

  const handlePredict = async () => {
    setLoading(true);
    setChatReply("");
    try {
      const res = await predictOutcome(form);
      setPrediction(res);
    } catch (err) {
      console.error(err);
      alert("Prediction failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const handleAskCounselor = async () => {
    if (!prediction) return;
    setLoading(true);
    try {
      const res = await askCounselor(prediction.dropout_risk_level, context);
      setChatReply(res.reply);
    } catch (err) {
      console.error(err);
      alert("Chatbot request failed.");
    } finally {
      setLoading(false);
    }
  };

  const riskColor = level =>
    level === "High" ? "#d9534f" : level === "Medium" ? "#f0ad4e" : "#5cb85c";

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <header style={{ display: "flex", justifyContent: "space-between", marginBottom: "1.5rem" }}>
        <h2>Student Dashboard</h2>
        <button onClick={onLogout}>Logout</button>
      </header>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "2rem",
        }}
      >
        {/* Left: data input + prediction */}
        <div style={{ border: "1px solid #ddd", padding: "1rem" }}>
          <h3>Enter Latest Academic Data</h3>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
            <div>
              <label>1st Sem Units Approved</label>
              <input
                type="number"
                name="curricular_units_1st_sem_approved"
                value={form.curricular_units_1st_sem_approved}
                onChange={handleChange}
                style={{ width: "100%" }}
              />
            </div>
            <div>
              <label>1st Sem Grade</label>
              <input
                type="number"
                name="curricular_units_1st_sem_grade"
                value={form.curricular_units_1st_sem_grade}
                onChange={handleChange}
                style={{ width: "100%" }}
              />
            </div>
            <div>
              <label>2nd Sem Units Approved</label>
              <input
                type="number"
                name="curricular_units_2nd_sem_approved"
                value={form.curricular_units_2nd_sem_approved}
                onChange={handleChange}
                style={{ width: "100%" }}
              />
            </div>
            <div>
              <label>2nd Sem Grade</label>
              <input
                type="number"
                name="curricular_units_2nd_sem_grade"
                value={form.curricular_units_2nd_sem_grade}
                onChange={handleChange}
                style={{ width: "100%" }}
              />
            </div>
            <div>
              <label>Admission Grade</label>
              <input
                type="number"
                name="admission_grade"
                value={form.admission_grade}
                onChange={handleChange}
                style={{ width: "100%" }}
              />
            </div>
            <div>
              <label>Age at Enrollment</label>
              <input
                type="number"
                name="age_at_enrollment"
                value={form.age_at_enrollment}
                onChange={handleChange}
                style={{ width: "100%" }}
              />
            </div>
          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            style={{ marginTop: "1rem", padding: "0.5rem 1rem" }}
          >
            {loading ? "Predicting..." : "Predict Dropout Risk"}
          </button>

          {prediction && (
            <div style={{ marginTop: "1rem" }}>
              <h4>Prediction Result</h4>
              <p>Status: <strong>{prediction.predicted_class}</strong></p>
              <p>
                Risk Level:{" "}
                <span style={{ color: riskColor(prediction.dropout_risk_level) }}>
                  {prediction.dropout_risk_level}
                </span>
              </p>
              <p>Probabilities:</p>
              <ul>
                {Object.entries(prediction.probabilities).map(([k, v]) => (
                  <li key={k}>
                    {k}: {(v * 100).toFixed(1)}%
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Right: chatbot */}
        <div style={{ border: "1px solid #ddd", padding: "1rem" }}>
          <h3>Counseling Chatbot</h3>
          <p>
            Describe your situation (e.g., attendance issues, stress, backlogs), then ask for guidance.
          </p>
          <textarea
            value={context}
            onChange={e => setContext(e.target.value)}
            rows={6}
            style={{ width: "100%", marginBottom: "0.75rem" }}
            placeholder="I am missing many maths classes and feel stressed before tests..."
          />
          <button
            onClick={handleAskCounselor}
            disabled={loading || !prediction}
            style={{ padding: "0.5rem 1rem" }}
          >
            {loading ? "Asking..." : "Ask Counselor"}
          </button>
          {chatReply && (
            <div style={{ marginTop: "1rem" }}>
              <h4>Counselor Reply</h4>
              <p>{chatReply}</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
