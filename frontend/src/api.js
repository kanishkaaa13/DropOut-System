import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export function getAuthHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function registerUser(email, password, role = "student") {
  const res = await axios.post(`${API_BASE}/auth/register`, {
    email,
    password,
    role,
  });
  return res.data; // { access_token, token_type }
}

export async function loginUser(email, password) {
  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);

  const res = await axios.post(`${API_BASE}/auth/login`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data; // { access_token, token_type }
}

export async function predictOutcome(payload) {
  const res = await axios.post(`${API_BASE}/predict/`, payload, {
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
  });
  return res.data; // PredictionResponse
}

export async function askCounselor(riskLevel, context) {
  const res = await axios.post(
    `${API_BASE}/chatbot/`,
    { student_risk_level: riskLevel, context },
    { headers: { "Content-Type": "application/json", ...getAuthHeaders() } }
  );
  return res.data; // { reply }
}
