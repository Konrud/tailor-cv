/**
 * SessionStorage utility functions for managing CV tailoring workflow state.
 *
 * These functions provide a type-safe interface for storing and retrieving
 * session data in the browser's SessionStorage API.
 */

import type { ProcessingSession } from "../types/session";

const SESSION_KEY = "tailorCV_session";

/**
 * Initialize a new processing session.
 */
export function initSession(): ProcessingSession {
  const session: ProcessingSession = {
    sessionId: crypto.randomUUID(),
    startedAt: new Date().toISOString(),
    currentStep: "upload_cv",
    errors: [],
  };

  saveSession(session);
  return session;
}

/**
 * Load the current session from SessionStorage.
 */
export function loadSession(): ProcessingSession | null {
  try {
    const data = sessionStorage.getItem(SESSION_KEY);
    if (!data) return null;

    return JSON.parse(data) as ProcessingSession;
  } catch (error) {
    console.error("Failed to load session:", error);
    return null;
  }
}

/**
 * Save the current session to SessionStorage.
 */
export function saveSession(session: ProcessingSession): void {
  try {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
  } catch (error) {
    console.error("Failed to save session:", error);
  }
}

/**
 * Update specific fields in the session.
 */
export function updateSession(updates: Partial<ProcessingSession>): void {
  const session = loadSession();
  if (!session) {
    console.warn("No active session to update");
    return;
  }

  const updatedSession = { ...session, ...updates };
  saveSession(updatedSession);
}

/**
 * Clear the current session (on user request or completion).
 */
export function clearSession(): void {
  sessionStorage.removeItem(SESSION_KEY);
}

/**
 * Get or create a session (ensures a session always exists).
 */
export function getOrCreateSession(): ProcessingSession {
  const existing = loadSession();
  return existing || initSession();
}

/**
 * Check if a session exists and is valid.
 */
export function hasActiveSession(): boolean {
  const session = loadSession();
  return session !== null;
}

