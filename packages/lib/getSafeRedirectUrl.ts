// Módulo replicado (acortado) de calcom/cal.diy -> packages/lib/getSafeRedirectUrl.ts
// Incluido para el análisis estático del repositorio real con SonarQube (Parte B).
// Se inlinean las constantes que en el repo real viven en @calcom/lib/constants
// para que el módulo sea auto-contenido; la lógica de seguridad es la original.

const CONSOLE_URL = "https://app.cal.com";
const WEBAPP_URL = "https://app.cal.com";
const WEBSITE_URL = "https://cal.com";

// It ensures that redirection URL safe where it is accepted through a query params or other means where user can change it.
export const getSafeRedirectUrl = (url = "") => {
  if (!url) {
    return null;
  }

  //It is important that this fn is given absolute URL because urls that don't start with HTTP can still deceive browser into redirecting to another domain
  if (url.search(/^https?:\/\//) === -1) {
    throw new Error("Pass an absolute URL");
  }

  const urlParsed = new URL(url);

  // Avoid open redirection security vulnerability
  if (![CONSOLE_URL, WEBAPP_URL, WEBSITE_URL].some((u) => new URL(u).origin === urlParsed.origin)) {
    url = `${WEBAPP_URL}/`;
  }

  return url;
};
