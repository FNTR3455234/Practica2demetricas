// Módulo replicado (tal cual) de calcom/cal.diy -> packages/lib/notEmpty.ts
// Incluido para el análisis estático del repositorio real con SonarQube (Parte B).

const notEmpty = <T>(value: T): value is NonNullable<typeof value> => !!value;

export default notEmpty;
