import type { Assessment, AssessmentIndex } from "../types/assessment";
import assessmentIndex from "./book1/assessments/index.json";
import section1 from "./book1/assessments/section-1.json";
import section2 from "./book1/assessments/section-2.json";
import section3 from "./book1/assessments/section-3.json";
import section4 from "./book1/assessments/section-4.json";
import finalTest from "./book1/assessments/final.json";

const byId: Record<string, Assessment> = {
  "section-1": section1 as Assessment,
  "section-2": section2 as Assessment,
  "section-3": section3 as Assessment,
  "section-4": section4 as Assessment,
  final: finalTest as Assessment,
};

export function getAssessmentIndex(): AssessmentIndex {
  return assessmentIndex as AssessmentIndex;
}

export function getAssessment(id: string): Assessment | undefined {
  return byId[id];
}

export function getSectionTest(section: number): Assessment | undefined {
  return byId[`section-${section}`];
}

export function getFinalTest(): Assessment | undefined {
  return byId.final;
}

export function listAssessments(): Assessment[] {
  const idx = getAssessmentIndex();
  return [...idx.sectionTests.map((id) => byId[id]), byId[idx.finalTest]].filter(
    Boolean
  );
}
