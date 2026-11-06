import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nosyra ProjectFlow · Nosyra Digital",
  description: "Nosyra ProjectFlow demo workspace by Nosyra Digital",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
