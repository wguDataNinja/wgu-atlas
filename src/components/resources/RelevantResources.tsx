import { getOfficialResourcePlacementsForSurface } from "@/lib/data";
import type {
  OfficialResourcePlacement,
  ResourceSurface,
} from "@/lib/types";

type Props = {
  surface: ResourceSurface;
  surfaceKey: string;
  className?: string;
};

const GROUP_LABELS: Record<string, string> = {
  outcomes: "Outcomes",
  accreditation: "Accreditation",
  regulatory_licensure: "Licensure & Exams",
  program_variant: "Specializations",
  program_guide: "Program Guides",
};

export default function RelevantResources({
  surface,
  surfaceKey,
  className = "",
}: Props) {
  const rows = getOfficialResourcePlacementsForSurface(surface, surfaceKey);
  if (rows.length === 0) return null;

  const grouped = groupByResourceGroup(rows);
  const contextLabel = surface === "program_detail" ? "degree" : "college";

  return (
    <section
      className={`rounded-lg border border-slate-200 bg-slate-50/60 p-4 ${className}`.trim()}
      aria-label="Relevant Resources"
    >
      <h2 className="text-sm font-semibold text-slate-800">Relevant Resources</h2>
      <p className="mt-1 text-xs text-slate-500">
        Official WGU resources related to this {contextLabel}.
      </p>

      <div className="mt-4 space-y-4">
        {grouped.map(({ group, items }) => (
          <div key={group}>
            {grouped.length > 1 && (
              <h3 className="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
                {GROUP_LABELS[group] ?? "Resources"}
              </h3>
            )}
            <ul className="space-y-2">
              {items.map((item) => (
                <li key={`${item.surface_key}::${item.resource_url}`}>
                  <a
                    href={item.resource_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-700 hover:underline"
                  >
                    {item.resource_title} <span aria-hidden="true">↗</span>
                  </a>
                  <p className="mt-0.5 text-xs text-slate-500">{item.benefit_reason}</p>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}

function groupByResourceGroup(rows: OfficialResourcePlacement[]) {
  const byGroup = new Map<string, OfficialResourcePlacement[]>();

  for (const row of rows) {
    if (!byGroup.has(row.resource_group)) {
      byGroup.set(row.resource_group, []);
    }
    byGroup.get(row.resource_group)!.push(row);
  }

  return [...byGroup.entries()]
    .map(([group, items]) => ({
      group,
      items: [...items].sort((a, b) => {
        if (a.display_priority !== b.display_priority) {
          return a.display_priority - b.display_priority;
        }
        return a.resource_title.localeCompare(b.resource_title);
      }),
      sortPriority: Math.min(...items.map((item) => item.display_priority)),
    }))
    .sort((a, b) => {
      if (a.sortPriority !== b.sortPriority) return a.sortPriority - b.sortPriority;
      return (GROUP_LABELS[a.group] ?? a.group).localeCompare(
        GROUP_LABELS[b.group] ?? b.group
      );
    });
}
