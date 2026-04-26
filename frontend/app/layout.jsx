import './globals.css';

export const metadata = {
  title: 'Mittu - Roadmap Generator',
  description: 'Personalized career roadmap generator with downloadable PDF.'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
