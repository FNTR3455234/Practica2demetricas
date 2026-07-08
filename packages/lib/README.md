# `packages/lib/` — módulos reales de cal.diy (para el análisis estático)

Estos archivos son **réplicas (acortadas) de módulos reales** del repositorio del
proyecto de la Unidad 1: [`calcom/cal.diy`](https://github.com/calcom/cal.diy),
tomados de su carpeta `packages/lib/`. Se incluyen **para que SonarQube analice
código real del proyecto** (no solo los Page Objects de las pruebas), cumpliendo
"análisis del repositorio" de la Parte B. Se mantiene la ruta original
`packages/lib/` para que corresponda al repositorio real.

> cal.diy es enorme y en TypeScript; por eso se copia solo un subconjunto
> representativo y, cuando un módulo dependía de otros paquetes internos, se
> acortó (inlineando constantes o usando `Date` nativo) conservando la lógica
> original. Cada archivo indica en su cabecera si es *tal cual* o *acortado*.

| Archivo | Origen en cal.diy | Estado | Por qué es interesante para Sonar |
|---|---|---|---|
| `slugify.ts` | `packages/lib/slugify.ts` | tal cual | Complejidad cognitiva alta (cadena de `.replace`), `@ts-ignore`. Genera slugs de *event-types*. |
| `text.ts` | `packages/lib/text.ts` | tal cual | Número mágico `148` en `truncateOnWord` (code smell / bug latente). |
| `random.ts` | `packages/lib/random.ts` | tal cual | Uso de `Math.random()` → *Security Hotspot* (aleatoriedad no criptográfica). |
| `getSafeRedirectUrl.ts` | `packages/lib/getSafeRedirectUrl.ts` | acortado | Protección contra *open redirect*; reasignación del parámetro `url`. Buen tema de seguridad. |
| `isOutOfBounds.ts` | `packages/lib/isOutOfBounds.tsx` | acortado | Guard de "reserva en el pasado" — mapea directo a la demo de booking. |
| `array.ts` | `packages/lib/array.ts` | tal cual | `uniqueBy` con `findIndex` anidado → complejidad / rendimiento. |
| `notEmpty.ts` | `packages/lib/notEmpty.ts` | tal cual | Type-guard genérico minimalista. |

## Nota de integridad

Estos módulos **no** se ejecutan ni se prueban con Selenium (las pruebas E2E
corren contra las demos locales de `app/`). Están aquí **exclusivamente como
código fuente a analizar** por SonarQube, y su origen queda documentado archivo
por archivo para no confundir autoría con la del equipo.
