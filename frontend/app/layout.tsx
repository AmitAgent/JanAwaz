import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "JanAwaz",
  description: "Independent help for citizens filing electricity complaints in Bihar.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
