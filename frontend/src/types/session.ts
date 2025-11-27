/**
 * TypeScript type definitions for SessionStorage.
 *
 * These types define the structure of data stored in the browser's SessionStorage
 * for managing CV tailoring workflow state.
 */

export type ProcessingStep =
  | "upload_cv"
  | "input_job"
  | "analyzing"
  | "tailoring"
  | "complete"
  | "error";

export interface SessionError {
  timestamp: string;
  step: ProcessingStep;
  errorType: string;
  message: string;
  technicalDetails?: string;
  retryable: boolean;
}

export interface CVSection {
  type: "summary" | "experience" | "education" | "skills" | "certifications" | "other";
  title: string;
  content: string;
  items: string[];
}

export interface MasterCV {
  id: string;
  fileName: string;
  fileType: "pdf" | "docx" | "txt";
  fileSize: number;
  uploadedAt: string;
  extractedText: string;
  parsedSections: CVSection[];
  language: "en";
  pageCount: number;
}

export interface RequiredSkill {
  name: string;
  category: "technical" | "soft" | "domain" | "tool" | "language";
  required: boolean;
  yearsExperience?: number;
}

export interface JobRequirements {
  title: string;
  company?: string;
  seniorityLevel?: string;
  skills: RequiredSkill[];
  responsibilities: string[];
  qualifications: string[];
  keywords: string[];
}

export interface JobDescription {
  id: string;
  source: "text" | "url";
  sourceUrl?: string;
  rawText: string;
  extractedAt: string;
  requirements: JobRequirements;
  language: "en";
  wordCount: number;
  platform?: "linkedin" | "indeed" | "glassdoor" | "other";
}

export interface MatchedSkill {
  skillName: string;
  matchConfidence: number;
  cvSource: string;
  jobRequirement: string;
}

export interface MissingSkill {
  skillName: string;
  importance: "required" | "preferred";
  category: string;
  suggestedAlternatives?: string[];
}

export interface RelevantExperience {
  cvSection: string;
  cvContent: string;
  jobResponsibility: string;
  relevanceScore: number;
}

export interface Warning {
  type: "low_match" | "minimal_job_info" | "processing_time";
  severity: "info" | "warning" | "error";
  message: string;
  recommendation?: string;
}

export interface GapAnalysis {
  id: string;
  cvId: string;
  jobId: string;
  createdAt: string;
  overallMatch: number;
  matchedSkills: MatchedSkill[];
  missingSkills: MissingSkill[];
  relevantExperience: RelevantExperience[];
  warnings: Warning[];
}

export interface Modification {
  section: string;
  modificationType: "rewrite" | "reorder" | "emphasis";
  original: string;
  modified: string;
  reason: string;
}

export interface KeywordMatch {
  keyword: string;
  incorporated: boolean;
  location: string;
  naturalness: number;
}

export interface TailoredCV {
  id: string;
  cvId: string;
  jobId: string;
  gapAnalysisId: string;
  createdAt: string;
  textVersion: string;
  pdfUrl: string;
  modifications: Modification[];
  keywordMatches: KeywordMatch[];
  processingTime: number;
  validationPassed: boolean;
}

export interface ProcessingSession {
  sessionId: string;
  startedAt: string;
  masterCV?: MasterCV;
  jobDescription?: JobDescription;
  gapAnalysis?: GapAnalysis;
  tailoredCV?: TailoredCV;
  currentStep: ProcessingStep;
  errors: SessionError[];
}

