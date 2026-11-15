// Hand-drawn cartoon/caricature portraits for the Office page — replaces
// plain emoji faces with an exaggerated comic style (messy hair, gritted
// teeth, sweat drops, KO eyes) that still reads clearly at small size.

const SKIN = { idle: "#f0c49a", busy: "#eab27e", error: "#cdb79a" };
const SHIRT = { idle: "#4f7dab", busy: "#c97b2e", error: "#7d7390" };
const HAIR = "#3a2b22";
const INK = "#2a241e";

function Sweat({ x, y }) {
  return <path d={`M${x} ${y} q4 6 0 10 q-4 -4 0 -10 Z`} fill="#8fd1ff" opacity="0.9" />;
}

function Spark({ x, y, scale = 1 }) {
  return (
    <path
      d={`M${x} ${y - 5 * scale} L${x + 1.4 * scale} ${y - 1.4 * scale} L${x + 5 * scale} ${y} L${x + 1.4 * scale} ${
        y + 1.4 * scale
      } L${x} ${y + 5 * scale} L${x - 1.4 * scale} ${y + 1.4 * scale} L${x - 5 * scale} ${y} L${
        x - 1.4 * scale
      } ${y - 1.4 * scale} Z`}
      fill="#ffd34d"
    />
  );
}

function Eyebrows({ mood }) {
  if (mood === "idle") {
    return (
      <>
        <path d="M38 40 q7 -5 14 0" stroke={INK} strokeWidth="3" fill="none" strokeLinecap="round" />
        <path d="M68 40 q7 -5 14 0" stroke={INK} strokeWidth="3" fill="none" strokeLinecap="round" />
      </>
    );
  }
  if (mood === "busy") {
    return (
      <>
        <path d="M37 38 L52 44" stroke={INK} strokeWidth="4" strokeLinecap="round" />
        <path d="M83 38 L68 44" stroke={INK} strokeWidth="4" strokeLinecap="round" />
      </>
    );
  }
  return (
    <>
      <path d="M35 30 L54 41" stroke={INK} strokeWidth="4" strokeLinecap="round" />
      <path d="M85 30 L66 41" stroke={INK} strokeWidth="4" strokeLinecap="round" />
    </>
  );
}

function Eyes({ mood }) {
  if (mood === "idle") {
    return (
      <>
        <path d="M40 50 q5 6 10 0" stroke={INK} strokeWidth="3" fill="none" strokeLinecap="round" />
        <path d="M70 50 q5 6 10 0" stroke={INK} strokeWidth="3" fill="none" strokeLinecap="round" />
      </>
    );
  }
  if (mood === "busy") {
    return (
      <>
        <circle cx="46" cy="51" r="6" fill="#fff" stroke={INK} strokeWidth="2" />
        <circle cx="46" cy="52" r="2.6" fill={INK} />
        <circle cx="74" cy="51" r="6" fill="#fff" stroke={INK} strokeWidth="2" />
        <circle cx="74" cy="52" r="2.6" fill={INK} />
        <path d="M39 59 q7 3 13 0" stroke={INK} strokeWidth="1.6" fill="none" opacity="0.5" />
        <path d="M68 59 q7 3 13 0" stroke={INK} strokeWidth="1.6" fill="none" opacity="0.5" />
      </>
    );
  }
  return (
    <>
      <path d="M40 45 L52 57 M52 45 L40 57" stroke={INK} strokeWidth="3.4" strokeLinecap="round" />
      <path d="M68 45 L80 57 M80 45 L68 57" stroke={INK} strokeWidth="3.4" strokeLinecap="round" />
    </>
  );
}

function Mouth({ mood }) {
  if (mood === "idle") {
    return <path d="M48 72 q12 10 24 0" stroke={INK} strokeWidth="3" fill="none" strokeLinecap="round" />;
  }
  if (mood === "busy") {
    return (
      <g>
        <rect x="47" y="70" width="26" height="10" rx="3" fill="#8a3b2e" />
        <path d="M49 70 v10 M55 70 v10 M61 70 v10 M67 70 v10" stroke="#fff" strokeWidth="2" />
      </g>
    );
  }
  return <ellipse cx="60" cy="76" rx="11" ry="9" fill="#6b2a22" />;
}

function Hair({ mood }) {
  if (mood === "idle") {
    return <path d="M30 40 q2 -28 30 -28 q28 0 30 28 q-14 -10 -30 -10 q-16 0 -30 10 Z" fill={HAIR} />;
  }
  if (mood === "busy") {
    return (
      <path
        d="M30 38 q2 -26 30 -26 q28 0 30 26 q-6 -14 -14 -8 q-6 -10 -16 -6 q-8 -8 -16 -2 q-8 -8 -14 2 Z"
        fill={HAIR}
      />
    );
  }
  return (
    <path
      d="M60 10 l3 14 l10 -10 l-3 13 l13 -6 l-8 11 l14 1 l-13 6 l10 9 l-14 -2 l5 13 l-11 -9 l-2 14 l-6 -13 l-8 11 l1 -14 l-13 5 l8 -11 l-14 -3 l13 -5 l-9 -11 l14 3 Z"
      fill={HAIR}
    />
  );
}

function Blush({ mood }) {
  if (mood === "busy") {
    return (
      <>
        <ellipse cx="38" cy="62" rx="6" ry="3.5" fill="#e8774f" opacity="0.5" />
        <ellipse cx="82" cy="62" rx="6" ry="3.5" fill="#e8774f" opacity="0.5" />
      </>
    );
  }
  return null;
}

/** A worker agent's portrait. `mood`: "idle" | "busy" | "error". */
export function WorkerCaricature({ mood }) {
  return (
    <svg viewBox="0 0 120 120" width="88" height="88" role="img" aria-label={`Trạng thái: ${mood}`}>
      <ellipse cx="60" cy="104" rx="36" ry="20" fill={SHIRT[mood]} />
      <circle cx="30" cy="54" r="7" fill={SKIN[mood]} />
      <circle cx="90" cy="54" r="7" fill={SKIN[mood]} />
      <circle cx="60" cy="54" r="30" fill={SKIN[mood]} />
      <Blush mood={mood} />
      <Eyebrows mood={mood} />
      <Eyes mood={mood} />
      <path d="M58 56 q-2 8 0 10" stroke="#c98a56" strokeWidth="2" fill="none" strokeLinecap="round" />
      <Mouth mood={mood} />
      <Hair mood={mood} />
      {mood === "busy" && <Sweat x={88} y={42} />}
      {mood === "error" && (
        <>
          <Sweat x={30} y={40} />
          <Sweat x={92} y={38} />
          <Sweat x={62} y={22} />
          <Spark x={18} y={30} scale={0.8} />
          <Spark x={104} y={62} scale={0.9} />
        </>
      )}
    </svg>
  );
}

/** The boss (Claude). `busy`: whether at least one worker is BUSY. */
export function BossCaricature({ busy }) {
  const mouth = busy ? "M46 76 q14 6 28 -2" : "M46 74 q14 12 28 0";
  return (
    <svg viewBox="0 0 120 120" width="104" height="104" role="img" aria-label="Sếp Claude">
      {!busy && (
        <>
          <path d="M18 60 q-10 -4 -8 -16" stroke="#e0ab73" strokeWidth="10" fill="none" strokeLinecap="round" />
          <path d="M102 60 q10 -4 8 -16" stroke="#e0ab73" strokeWidth="10" fill="none" strokeLinecap="round" />
        </>
      )}
      <ellipse cx="60" cy="100" rx="48" ry="32" fill="#2d3b55" />
      <circle cx="60" cy="88" r="4" fill="#d8b24a" />
      <circle cx="60" cy="100" r="4" fill="#d8b24a" />
      <path d="M60 68 L52 112 L68 112 Z" fill="#b5342a" />
      {busy && (
        <path d="M100 70 q16 -4 18 -18" stroke="#e0ab73" strokeWidth="11" fill="none" strokeLinecap="round" />
      )}
      {busy && <circle cx="120" cy="50" r="6" fill="#e0ab73" />}

      <path d="M24 44 q-2 -22 36 -24 q38 2 36 24 q4 10 -4 16 q2 -18 -32 -18 q-34 0 -32 18 q-8 -6 -4 -16Z" fill={HAIR} />
      <ellipse cx="60" cy="52" rx="30" ry="28" fill="#eab27e" />
      <ellipse cx="46" cy="30" rx="6" ry="3" fill="#ffffff" opacity="0.35" />

      {busy ? (
        <>
          <path d="M38 42 q7 -6 15 -1" stroke={INK} strokeWidth="3.4" fill="none" strokeLinecap="round" />
          <path d="M82 42 q-7 -6 -15 -1" stroke={INK} strokeWidth="3.4" fill="none" strokeLinecap="round" />
          <circle cx="46" cy="50" r="5" fill="#fff" stroke={INK} strokeWidth="2" />
          <circle cx="48" cy="50" r="2.2" fill={INK} />
          <circle cx="74" cy="50" r="5" fill="#fff" stroke={INK} strokeWidth="2" />
          <circle cx="76" cy="50" r="2.2" fill={INK} />
        </>
      ) : (
        <>
          <path d="M37 44 q9 -8 16 0" stroke={INK} strokeWidth="3.4" fill="none" strokeLinecap="round" />
          <path d="M83 44 q-9 -8 -16 0" stroke={INK} strokeWidth="3.4" fill="none" strokeLinecap="round" />
          <path d="M39 50 q7 7 14 0" stroke={INK} strokeWidth="3" fill="none" strokeLinecap="round" />
          <path d="M67 50 q7 7 14 0" stroke={INK} strokeWidth="3" fill="none" strokeLinecap="round" />
        </>
      )}

      <path d="M46 62 q14 6 28 0 q-2 6 -14 6 q-12 0 -14 -6 Z" fill="#5a3a26" />
      <path d={mouth} stroke={INK} strokeWidth="2.6" fill="none" strokeLinecap="round" />

      {!busy && (
        <g opacity="0.8">
          <rect x="94" y="94" width="14" height="12" rx="2" fill="#e7e2d8" />
          <path d="M108 97 q6 0 6 5 q0 5 -6 5" stroke="#e7e2d8" strokeWidth="2.4" fill="none" />
          <path d="M98 90 q2 -4 0 -7 M102 90 q2 -4 0 -7" stroke="#cfcabf" strokeWidth="1.6" fill="none" strokeLinecap="round" />
        </g>
      )}
    </svg>
  );
}
