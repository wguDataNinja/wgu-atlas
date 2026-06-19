import type { Metadata } from "next";
import "./globals.css";
import Nav from "@/components/layout/Nav";
import Footer from "@/components/layout/Footer";
import { getHomepageSummary } from "@/lib/data";

export const metadata: Metadata = {
  title: {
    default: "WGU Atlas",
    template: "%s | WGU Atlas",
  },
  description:
    "An independent guide to WGU degrees, courses, and colleges, built from public WGU sources.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { archive_span, data_date } = getHomepageSummary();
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">
        <Nav />
        <main className="flex-1">{children}</main>
        <Footer archiveSpan={archive_span} dataDate={data_date} />
      </body>
    </html>
  );
}
