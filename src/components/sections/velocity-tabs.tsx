"use client";

import { useLayoutEffect } from "react";
import { isDraftAnchor } from "@/data/draft-chart-links";
import { SubTabs } from "@/components/sub-tabs";
import { VelocityInstrumentsSection } from "@/components/sections/velocity-instruments-section";
import { ExpectationsSection } from "@/components/sections/expectations-section";
import { DraftChartsSection } from "@/components/sections/draft-charts-section";
import { usePerformanceHash, navigatePerformance, revealDraftTarget } from "@/lib/field-velocity/navigation";

export function VelocityTabs({ performance }: { performance: React.ReactNode }) {
  const hash = usePerformanceHash();
  useLayoutEffect(() => revealDraftTarget(hash.slice(1)), [hash]);
  return (
    <SubTabs
      selectedKey={isDraftAnchor(hash.slice(1)) ? "draft-charts" : hash === "#expectations" ? "expectations" : "instruments"}
      onSelect={key => navigatePerformance(key === "expectations" ? "expectations" : key === "draft-charts" ? "draft-charts" : "performance_curves")}
      tabs={[
        { key: "instruments", label: "Metrics", node: <VelocityInstrumentsSection performance={performance} /> },
        { key: "expectations", label: "Expectations", node: <ExpectationsSection /> },
        { key: "draft-charts", label: "Draft charts", node: <DraftChartsSection /> },
      ]}
    />
  );
}
