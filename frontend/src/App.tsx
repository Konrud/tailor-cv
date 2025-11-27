/**
 * AI CV Tailor - Root Application Component.
 *
 * This component sets up React Router, TanStack Query provider,
 * and global application layout.
 */

import { QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { queryClient } from "./services/api";
import "./styles/global.css";

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="app">
          <Routes>
            <Route
              path="/"
              element={
                <div className="container" style={{ padding: "2rem", textAlign: "center" }}>
                  <h1>AI CV Tailor</h1>
                  <p>AI-powered CV tailoring for job applications</p>
                  <p style={{ color: "var(--color-text-muted)", marginTop: "2rem" }}>
                    Application setup complete. Implement user stories to add functionality.
                  </p>
                </div>
              }
            />
            <Route
              path="*"
              element={
                <div className="container" style={{ padding: "2rem", textAlign: "center" }}>
                  <h1>404 - Page Not Found</h1>
                  <p>The page you're looking for doesn't exist.</p>
                  <a href="/">Go Home</a>
                </div>
              }
            />
          </Routes>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;

