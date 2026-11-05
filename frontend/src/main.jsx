
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from "./App.jsx";
import "./App.css";

// 取得 HTML 中的 React Root 元素
const rootElement = document.getElementById("root");

// 確認 Root 元素存在
if (!rootElement) {
  throw new Error("Root element not found");
}

// 建立 React Application
createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
