// Módulo replicado (acortado) de calcom/cal.diy -> packages/lib/isOutOfBounds.tsx
// Incluido para el análisis estático del repositorio real con SonarQube (Parte B).
// Se conserva el guard de "reserva en el pasado" y el chequeo de minimum booking
// notice (que es justo lo que valida nuestra demo de booking). Para que el módulo
// sea auto-contenido se usa Date nativo en lugar de dayjs; la lógica es la original.

export class BookingDateInPastError extends Error {
  constructor(message = "Attempting to book a meeting in the past.") {
    super(message);
  }
}

function guardAgainstBookingInThePast(date: Date) {
  if (date >= new Date()) {
    // Date is in the future.
    return;
  }
  throw new BookingDateInPastError();
}

/**
 * To be used when we work on Timeslots(and not Dates) to check boundaries
 * It ensures that the time isn't in the past and also checks if the time is within the minimum booking notice.
 * Note: It throws error that needs to be caught by caller.
 */
export function isTimeOutOfBounds({
  time,
  minimumBookingNotice,
}: {
  time: string | number | Date;
  minimumBookingNotice?: number;
}) {
  const date = new Date(time);

  guardAgainstBookingInThePast(date);

  if (minimumBookingNotice) {
    const minimumBookingStartDate = new Date(Date.now() + minimumBookingNotice * 60 * 1000);
    if (date < minimumBookingStartDate) {
      return true;
    }
  }

  return false;
}

/**
 * Wrapper over isTimeOutOfBounds to return a status object.
 * Note: It doesn't throw any error and can be safely used
 */
export function getPastTimeAndMinimumBookingNoticeBoundsStatus({
  time,
  minimumBookingNotice,
}: {
  time: string | number | Date;
  minimumBookingNotice?: number;
}): {
  isOutOfBounds: boolean;
  reason: "minBookNoticeViolation" | "slotInPast" | null;
} {
  try {
    const isOutOfBounds = isTimeOutOfBounds({ time, minimumBookingNotice });
    return {
      isOutOfBounds,
      reason: isOutOfBounds ? "minBookNoticeViolation" : null,
    };
  } catch (error) {
    if (error instanceof BookingDateInPastError) {
      return {
        isOutOfBounds: true,
        reason: "slotInPast",
      };
    }
    throw error;
  }
}
