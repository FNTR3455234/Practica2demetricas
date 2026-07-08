// Módulo replicado (tal cual) de calcom/cal.diy -> packages/lib/array.ts
// Incluido para el análisis estático del repositorio real con SonarQube (Parte B).

export const notUndefined = <T>(val: T | undefined): val is T => Boolean(val);
export const uniqueBy = <T extends { [key: string]: unknown }>(array: T[], keys: (keyof T)[]) => {
  return array.filter(
    (item, index, self) => index === self.findIndex((t) => keys.every((key) => t[key] === item[key]))
  );
};
