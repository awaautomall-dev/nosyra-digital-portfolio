import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nosyra Digital | Business Software",
  description:
    "Choose a Nosyra Digital workspace for customer relationships, inventory, or project management.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
