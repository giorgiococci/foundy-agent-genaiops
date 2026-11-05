import type { PlanningContext } from "./api.ts";

export function entityName(id: string, context?: PlanningContext): string {
  const label = context?.labels[id];
  return label ? `${label} (${id})` : id;
}

export function formatCost(value: number, context?: PlanningContext): string {
  return context
    ? new Intl.NumberFormat("en-GB", { style: "currency", currency: context.currency }).format(value)
    : `${value} cost units (currency unspecified)`;
}

export function formatSchedule(day: number, calendarDate?: string): string {
  return calendarDate
    ? new Intl.DateTimeFormat("en-GB", {
      day: "numeric", month: "short", year: "numeric", timeZone: "UTC",
    }).format(new Date(`${calendarDate}T00:00:00Z`))
    : `Scenario day ${day} (calendar date unspecified)`;
}

export function formatMargin(days: number): string {
  if (days === 0) return "on the deadline, no buffer";
  return days > 0 ? `${days}-day buffer` : `${-days} ${days === -1 ? "day" : "days"} late`;
}
