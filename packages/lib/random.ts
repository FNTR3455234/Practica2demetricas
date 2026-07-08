// Módulo replicado (tal cual) de calcom/cal.diy -> packages/lib/random.ts
// Incluido para el análisis estático del repositorio real con SonarQube (Parte B).

const CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
const CHARACTERS_LENGTH = CHARACTERS.length;

/**
 * Generate a random string of a given length using alphanumeric characters.
 */
export const randomString = function (length = 12) {
  let result = "";

  for (let i = 0; i < length; i++) {
    result += CHARACTERS.charAt(Math.floor(Math.random() * CHARACTERS_LENGTH));
  }

  return result;
};
