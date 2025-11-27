/**
 * Client-side validation helpers.
 *
 * These functions provide validation logic for user inputs before API submission.
 */

/**
 * Validate file size (max 5 MB per FR-001).
 */
export function validateFileSize(file: File, maxSizeMB: number = 5): string | null {
  const maxBytes = maxSizeMB * 1024 * 1024;

  if (file.size > maxBytes) {
    return `File size exceeds ${maxSizeMB} MB limit. Please upload a smaller file.`;
  }

  return null;
}

/**
 * Validate file type (PDF, DOCX, TXT per FR-001b).
 */
export function validateFileType(file: File): string | null {
  const allowedTypes = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
  ];
  const allowedExtensions = [".pdf", ".docx", ".txt"];

  const fileExtension = file.name.toLowerCase().slice(file.name.lastIndexOf("."));

  if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
    return "Invalid file type. Please upload a PDF, DOCX, or TXT file.";
  }

  return null;
}

/**
 * Validate job description text (min 10 chars, max 2500 words per FR-028).
 */
export function validateJobDescriptionText(text: string): string | null {
  if (text.trim().length < 10) {
    return "Job description must be at least 10 characters.";
  }

  const wordCount = text.trim().split(/\s+/).length;
  if (wordCount > 2500) {
    return `Job description exceeds 2500 words (currently ${wordCount} words). Please shorten it.`;
  }

  return null;
}

/**
 * Validate URL format.
 */
export function validateURL(url: string): string | null {
  try {
    new URL(url);
    return null;
  } catch {
    return "Invalid URL format. Please enter a valid job posting URL.";
  }
}

/**
 * Validate job URL platform (LinkedIn, Indeed, Glassdoor supported).
 */
export function validateJobURL(url: string): string | null {
  const urlValidation = validateURL(url);
  if (urlValidation) return urlValidation;

  const supportedPlatforms = ["linkedin.com", "indeed.com", "glassdoor.com"];
  const hostname = new URL(url).hostname.toLowerCase();

  const isSupported = supportedPlatforms.some((platform) => hostname.includes(platform));

  if (!isSupported) {
    return "We currently support LinkedIn, Indeed, and Glassdoor job URLs. You can paste the job description text instead.";
  }

  return null;
}

/**
 * Validate email format (optional, for future features).
 */
export function validateEmail(email: string): string | null {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailRegex.test(email)) {
    return "Invalid email format.";
  }

  return null;
}

/**
 * Generic required field validator.
 */
export function validateRequired(value: string, fieldName: string): string | null {
  if (!value || value.trim().length === 0) {
    return `${fieldName} is required.`;
  }

  return null;
}

