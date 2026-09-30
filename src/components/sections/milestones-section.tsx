import { SectionIntro } from "@/components/sections/section-intro";
import { MilestoneTimeline } from "@/components/milestone-timeline";

export function MilestonesSection() {
  return (
    <>
      <SectionIntro title="Milestone timeline">
        Tracked deals, partnerships, first-in-human trials, and regulatory milestones across
        neural interfaces and neurotechnology, on one shared time axis — color marks the
        stage. Filter by BCI only or view the broader neurotech ecosystem.
        Click a year to focus it. The focused year is wider than the column: a bar under the lanes, and Later months, reach the rest of the year. On desktop, fold the side panel to see the whole year without scrolling.
        Click a stage in the legend to expand its subcategories and filter by any subset;
        hover any logo for details, including spelled-out regulatory markers; click to open the
        primary source. Anything without a confirmed date sits in the &apos;date TBD&apos; shelf
        rather than being faked onto the axis.
      </SectionIntro>
      <MilestoneTimeline />
      <p className="mt-4 text-xs leading-relaxed text-faint">
        2026 events: Q1+ 2026 BCI Market Map by Neurotech Futures &amp; PL Neuro
        (bit.ly/Q126BCImemo), enriched with primary-source announcement dates, plus
        later 2026 events added only when a company release names the date.
        2024–2025 pathway events: screened from the Neurotech Futures regulatory
        digests, mapped onto the same clinical / commercial lanes.
      </p>
    </>
  );
}
