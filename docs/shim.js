// Small stand-in for the dashboard runtime the charts were first written for: loads the CSV once,
// runs the derived tables ("calcs") in order, and redraws every chart on load and on resize.
(() => {
  const calcs = [], drawers = new Map(), store = {};
  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  window.dash = {
    get colors() { return [css('--series-1'), css('--series-2'), css('--series-3')]; },
    calc(id, spec) { calcs.push([id, spec]); },
    data(id) { return store[id] ? {status: 'ok', data: store[id]} : {status: 'loading', data: []}; },
    draw(name, fn) {
      if (fn) drawers.set(name, fn);
      const f = drawers.get(name);
      if (f) document.querySelectorAll(`[data-draw="${name}"]`).forEach((el) => f(el));
    },
  };
  const drawAll = () => drawers.forEach((_, name) => dash.draw(name));
  d3.csv('data/apt_bulletin_articles.csv').then((rows) => {
    store.articles = rows;
    for (const [id, spec] of calcs) store[id] = spec.fn(...spec.inputs.map((i) => store[i]));
    drawAll();
    let w = window.innerWidth;
    window.addEventListener('resize', () => { if (window.innerWidth !== w) { w = window.innerWidth; drawAll(); } });
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', drawAll);
  }).catch((e) => {
    document.querySelectorAll('[data-draw]').forEach((el) => { el.textContent = 'The data file did not load.'; });
    console.error(e);
  });
})();
