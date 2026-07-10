// Módulo replicado (tal cual) de calcom/cal.diy -> packages/lib/random.ts
// Incluido para el análisis estático del repositorio real con SonarQube (Parte B).

const CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
const CHARACTERS_LENGTH = CHARACTERS.length;


export const randomString = function (length = 12) {
  const bytes = new Uint32Array(length);
  crypto.getRandomValues(bytes);

  let result = "";
  for (let i = 0; i < length; i++) {
    result += CHARACTERS.charAt(bytes[i] % CHARACTERS_LENGTH);
  }

  return result;
};
