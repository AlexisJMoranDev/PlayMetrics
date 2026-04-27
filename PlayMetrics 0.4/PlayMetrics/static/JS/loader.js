(function () {

  document.body.style.visibility = 'hidden';

  /* ── 2. Crear e insertar el overlay ─────────────────────── */
  const overlay = document.createElement('div');
  overlay.id = 'pm-loader';
  overlay.innerHTML = `
    <canvas id="pm-canvas" width="380" height="160"></canvas>
    <div id="pm-ui">
      <div id="pm-text">Iniciando...</div>
      <div id="pm-bar-wrap"><div id="pm-bar"></div></div>
      <div id="pm-pct">0%</div>
    </div>
  `;
  document.body.prepend(overlay);

  /* Mostrar body ahora que el overlay ya está encima */
  document.body.style.visibility = 'visible';

  /* ── 3. Canvas & píxeles ────────────────────────────────── */
  const canvas = document.getElementById('pm-canvas');
  const ctx    = canvas.getContext('2d');

  const SZ   = 8;
  const GAP  = 2;
  const STEP = SZ + GAP;

  const glyphs = {
    P: [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]],
    L: [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
    A: [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]],
    Y: [[1,0,0,0,1],[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
    M: [[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]],
    E: [[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
    T: [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
    R: [[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0],[1,0,1,0,0],[1,0,0,1,0],[1,0,0,0,1]],
    I: [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,1,1]],
    C: [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,1],[0,1,1,1,0]],
    S: [[0,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[0,1,1,1,0],[0,0,0,0,1],[0,0,0,0,1],[1,1,1,1,0]],
  };

  const word1 = ['P','L','A','Y'];
  const word2 = ['M','E','T','R','I','C','S'];

  function lineWidth(letters) {
    let w = 0;
    letters.forEach((ch, i) => {
      w += glyphs[ch][0].length + (i < letters.length - 1 ? 1 : 0);
    });
    return w * STEP - GAP;
  }

  function buildPixels(letters, offsetX, offsetY) {
    const pixels = [];
    let cx = offsetX;
    letters.forEach(ch => {
      const g = glyphs[ch];
      const w = g[0].length;
      for (let row = 0; row < 7; row++) {
        for (let col = 0; col < w; col++) {
          if (g[row][col]) {
            pixels.push({
              x: cx + col * STEP,
              y: offsetY + row * STEP,
              delay: Math.random() * 1200
            });
          }
        }
      }
      cx += (w + 1) * STEP;
    });
    return pixels;
  }

  const cw  = canvas.width;
  const ox1 = Math.floor((cw - lineWidth(word1)) / 2);
  const ox2 = Math.floor((cw - lineWidth(word2)) / 2);

  const allPixels = [
    ...buildPixels(word1, ox1, 2),
    ...buildPixels(word2, ox2, 2 + 7 * STEP + 4)
  ];

  /* ── 4. Helpers ─────────────────────────────────────────── */
  function hexToRgb(hex) {
    return [
      parseInt(hex.slice(1,3), 16),
      parseInt(hex.slice(3,5), 16),
      parseInt(hex.slice(5,7), 16)
    ];
  }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function easeOut(t)     { return 1 - Math.pow(1 - t, 3); }

  const goldRgb = hexToRgb('#D4A742');
  const dimRgb  = hexToRgb('#2A220A');

  const msgs = [
    'Iniciando...',
    'Cargando modelo...',
    'Procesando tags...',
    'Calibrando métricas...',
    'Listo'
  ];

  /* ── 5. Lógica de cierre ────────────────────────────────── */

  const ANIM_MIN = 2400;
  const SHIMMER_START = 1800;
  let start     = null;
  let pageReady = false;
  let animDone  = false;

  window.addEventListener('load', () => {
    pageReady = true;
    tryClose();
  });

  function tryClose() {
    if (!pageReady || !animDone) return;
    overlay.style.transition = 'opacity 0.6s ease';
    overlay.style.opacity    = '0';
    setTimeout(() => overlay.remove(), 650);
  }

  /* ── 6. Loop de animación ───────────────────────────────── */
  function draw(ts) {
    if (!start) start = ts;
    const elapsed      = ts - start;
    const animProgress = Math.min(elapsed / ANIM_MIN, 1);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    /* Píxeles encendiéndose */
    allPixels.forEach(p => {
      const pe = elapsed - p.delay;
      const t  = pe > 0 ? Math.min(easeOut(pe / 500), 1) : 0;
      const r  = Math.round(lerp(dimRgb[0], goldRgb[0], t));
      const g  = Math.round(lerp(dimRgb[1], goldRgb[1], t));
      const b  = Math.round(lerp(dimRgb[2], goldRgb[2], t));
      ctx.fillStyle = `rgb(${r},${g},${b})`;
      ctx.beginPath();
      ctx.roundRect(p.x, p.y, SZ, SZ, 1.5);
      ctx.fill();
    });

    /* Shimmer */
    if (elapsed > SHIMMER_START) {
      const shimmerX = ((elapsed - SHIMMER_START) % 1200) / 1200 * canvas.width;
      allPixels.forEach(p => {
        const dist = Math.abs(p.x - shimmerX);
        if (dist < 24) {
          const glow = 1 - dist / 24;
          ctx.fillStyle = `rgb(
            ${Math.round(lerp(goldRgb[0], 255, glow * 0.5))},
            ${Math.round(lerp(goldRgb[1], 220, glow * 0.4))},
            ${Math.round(lerp(goldRgb[2], 130, glow * 0.3))}
          )`;
          ctx.beginPath();
          ctx.roundRect(p.x, p.y, SZ, SZ, 1.5);
          ctx.fill();
        }
      });
    }

    /* Barra y texto */
    const pct = Math.min(Math.round(animProgress * 100), 100);
    document.getElementById('pm-bar').style.width  = pct + '%';
    document.getElementById('pm-pct').textContent  = pct + '%';
    const idx = Math.min(Math.floor(animProgress * msgs.length), msgs.length - 1);
    document.getElementById('pm-text').textContent = msgs[idx];

    if (animProgress < 1) {
      requestAnimationFrame(draw);
    } else {
      animDone = true;
      tryClose();
    }
  }

  requestAnimationFrame(draw);

})();