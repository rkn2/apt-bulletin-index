  dash.calc('committee_totals', {
    title: 'Items per committee',
    description: 'Counts articles and Practice Points tagged to each committee, and their share of all items.',
    inputs: ['articles'],
    fn: (articles) => {
      const C = [['mat', 'Materials (TCM)'], ['doc', 'Documentation (TC-Doc)'], ['petc', 'Preservation engineering (PETC)'], ['sp', 'Sustainable preservation (TC-SP)'], ['codes', 'Codes and standards'], ['mh', 'Modern heritage (TC-MH)'], ['dis', 'Disaster (part of PETC)']];
      const total = articles.length;
      return C.map(([key, committee]) => {
        const tagged = articles.filter((a) => a[key] === '1');
        const pps = tagged.filter((a) => a.kind === 'Practice Point').length;
        return {key, committee, items: tagged.length, articles: tagged.length - pps, practice_points: pps, share: tagged.length / total};
      }).sort((a, b) => b.items - a.items);
    },
  });

  dash.calc('overview', {
    title: 'Headline figures',
    description: 'Total items and the largest and smallest technical committee by share (Disaster, a PETC subgroup, is not compared).',
    inputs: ['committee_totals', 'articles'],
    fn: (committee_totals, articles) => {
      const s = committee_totals.filter((c) => c.key !== 'dis').sort((a, b) => b.share - a.share);
      return [{total: articles.length, top_committee: s[0].committee, top_share: s[0].share, low_committee: s[s.length - 1].committee, low_share: s[s.length - 1].share}];
    },
  });

  dash.calc('decade_shares', {
    title: 'Committee share by decade',
    description: 'For each decade, the share of items tagged to each committee (1969 counted with the 1970s).',
    inputs: ['articles'],
    fn: (articles) => {
      const C = [['mat', 'Materials'], ['doc', 'Documentation'], ['petc', 'Preservation eng.'], ['sp', 'Sustainable'], ['codes', 'Codes and standards'], ['mh', 'Modern heritage'], ['dis', 'Disaster (PETC)']];
      const dec = (y) => (Number(y) < 1980 ? '1969–79' : `${Math.floor(Number(y) / 10) * 10}s`);
      const groups = d3.group(articles, (a) => dec(a.year));
      const out = [];
      for (const [decade, rows] of [...groups].sort((a, b) => d3.ascending(a[0], b[0]))) {
        for (const [key, committee] of C) {
          const n = rows.filter((a) => a[key] === '1').length;
          out.push({decade, key, committee, items: n, total: rows.length, share: n / rows.length});
        }
      }
      return out;
    },
  });

  dash.calc('discipline_decades', {
    title: 'Discipline share by decade',
    description: 'For each decade, the share of items tagged engineering, architecture or conservation (1969 counted with the 1970s).',
    inputs: ['articles'],
    fn: (articles) => {
      const D = [['eng', 'Engineering'], ['arch', 'Architecture'], ['cons', 'Conservation']];
      const dec = (y) => (Number(y) < 1980 ? '1969–79' : `${Math.floor(Number(y) / 10) * 10}s`);
      const groups = d3.group(articles, (a) => dec(a.year));
      const out = [];
      for (const [decade, rows] of [...groups].sort((a, b) => d3.ascending(a[0], b[0]))) {
        for (const [key, discipline] of D) {
          const n = rows.filter((a) => a[key] === '1').length;
          out.push({decade, key, discipline, items: n, total: rows.length, share: n / rows.length});
        }
      }
      return out;
    },
  });

  dash.calc('item_tags', {
    title: 'Tags per item',
    description: 'Each item\'s committee and discipline tags as readable text.',
    inputs: ['articles'],
    fn: (articles) => {
      const C = [['doc', 'TC-Doc'], ['mat', 'TCM'], ['petc', 'PETC'], ['codes', 'Codes'], ['mh', 'TC-MH'], ['sp', 'TC-SP'], ['dis', 'PETC: disaster']];
      const D = [['eng', 'Engineering'], ['arch', 'Architecture'], ['cons', 'Conservation']];
      return articles.map((a) => ({
        id: a.id,
        committees: C.filter(([k]) => a[k] === '1').map(([, l]) => l).join(', '),
        disciplines: D.filter(([k]) => a[k] === '1').map(([, l]) => l).join(', '),
      }));
    },
  });

  const num = d3.format(',');
  const pct = d3.format('.0%');
  const NS = 'http://www.w3.org/2000/svg';


  const tipFor = (el) => {
    const t = document.createElement('div');
    t.className = 'tip'; t.hidden = true; el.append(t);
    return {
      show(lines, x, y) {
        t.replaceChildren(...lines.map(([cls, text]) => { const d = document.createElement('div'); if (cls) d.className = cls; d.textContent = text; return d; }));
        t.hidden = false;
        const w = el.clientWidth, tw = t.offsetWidth;
        t.style.left = `${Math.max(0, Math.min(w - tw, x + 12))}px`;
        t.style.top = `${Math.max(0, y - t.offsetHeight - 8)}px`;
      },
      hide() { t.hidden = true; },
    };
  };
  const textWidth = (svg, s) => {
    const t = document.createElementNS(NS, 'text'); t.textContent = s; svg.append(t);
    const w = t.getComputedTextLength(); t.remove(); return w;
  };
  const ok = (id) => dash.data(id).status === 'ok';
  const reset = (el) => { el.replaceChildren(); };

  // Header figures
  const ov = () => dash.data('overview');
  dash.draw('total', (el) => { el.textContent = ok('overview') ? num(ov().data[0].total) : '—'; });
  dash.draw('top-share', (el) => { el.textContent = ok('overview') ? pct(ov().data[0].top_share) : '—'; });
  dash.draw('top-name', (el) => { el.textContent = ok('overview') ? ov().data[0].top_committee : '—'; });
  dash.draw('low-name', (el) => { el.textContent = ok('overview') ? ov().data[0].low_committee : '—'; });
  dash.draw('low-share', (el) => { el.textContent = ok('overview') ? pct(ov().data[0].low_share) : '—'; });

  // Committee bars: label line above each bar, value at the right
  dash.draw('committee-bars', (el) => {
    if (!ok('committee_totals')) return reset(el);
    const rows = dash.data('committee_totals').data;
    el.replaceChildren();
    const W = Math.max(260, el.clientWidth), rowH = 46, H = rows.length * rowH;
    const svg = d3.select(el).append('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    const x = d3.scaleLinear([0, d3.max(rows, (r) => r.items)], [0, W]);
    const tip = tipFor(el);
    const g = svg.selectAll('g').data(rows).join('g').attr('transform', (_, i) => `translate(0,${i * rowH})`);
    g.append('text').attr('x', 0).attr('y', 14).text((r) => r.committee);
    g.append('text').attr('x', W).attr('y', 14).attr('text-anchor', 'end').attr('class', 'muted').text((r) => `${num(r.items)} · ${pct(r.share)}`);
    g.append('rect').attr('x', 0).attr('y', 22).attr('height', 14).attr('rx', 3).attr('width', (r) => x(r.articles)).attr('fill', dash.colors[0]);
    g.append('rect').attr('x', (r) => x(r.articles)).attr('y', 22).attr('height', 14).attr('width', (r) => x(r.practice_points)).attr('fill', dash.colors[1]);
    g.append('rect').attr('x', 0).attr('y', 0).attr('width', W).attr('height', rowH).attr('fill', 'transparent')
      .on('mousemove', (e, r) => { const [mx, my] = d3.pointer(e, el); tip.show([['k', r.committee], ['', `${num(r.articles)} articles`], ['', `${num(r.practice_points)} Practice Points`], ['', `${pct(r.share)} of all items`]], mx, my); })
      .on('mouseleave', () => tip.hide());
  });

  // Heatmap: committees x decades
  dash.draw('decade-heat', (el) => {
    if (!ok('decade_shares')) return reset(el);
    const rows = dash.data('decade_shares').data;
    el.replaceChildren();
    const decades = [...new Set(rows.map((r) => r.decade))];
    const comms = [...new Set(rows.map((r) => r.committee))];
    const W = Math.max(280, el.clientWidth);
    const svg = d3.select(el).append('svg').attr('width', '100%');
    const left = d3.max(comms, (c) => textWidth(svg.node(), c)) + 10, top = 22, cellH = 36;
    const cw = (W - left) / decades.length, H = top + comms.length * cellH;
    svg.attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    const max = d3.max(rows, (r) => r.share);
    const tip = tipFor(el);
    svg.selectAll('text.col').data(decades).join('text').attr('class', 'col muted').attr('x', (_, i) => left + i * cw + cw / 2).attr('y', 14).attr('text-anchor', 'middle').text((d) => (cw < 52 ? d.replace(/^19(\d\d)–79$/, "'$1–79").replace(/^(\d\d)(\d\d)s$/, "'$2s") : d));
    svg.selectAll('text.row').data(comms).join('text').attr('class', 'row').attr('x', 0).attr('y', (_, i) => top + i * cellH + cellH / 2 + 4).text((d) => d);
    const cell = svg.selectAll('g.cell').data(rows).join('g').attr('class', 'cell')
      .attr('transform', (r) => `translate(${left + decades.indexOf(r.decade) * cw},${top + comms.indexOf(r.committee) * cellH})`);
    cell.append('rect').attr('x', 1).attr('y', 1).attr('width', cw - 2).attr('height', cellH - 2).attr('rx', 3)
      .attr('fill', dash.colors[0]).attr('fill-opacity', (r) => 0.06 + 0.94 * (r.share / max));
    cell.append('text').attr('x', cw / 2).attr('y', cellH / 2 + 4).attr('text-anchor', 'middle')
      .style('fill', (r) => (r.share / max > 0.55 ? 'var(--color-bg)' : 'var(--color-fg)')).text((r) => pct(r.share));
    cell.on('mousemove', (e, r) => { const [mx, my] = d3.pointer(e, el); tip.show([['k', `${r.committee}, ${r.decade}`], ['', `${num(r.items)} of ${num(r.total)} items (${pct(r.share)})`]], mx, my); })
      .on('mouseleave', () => tip.hide());
  });

  // Discipline lines with end labels
  dash.draw('disc-lines', (el) => {
    if (!ok('discipline_decades')) return reset(el);
    const rows = dash.data('discipline_decades').data;
    el.replaceChildren();
    const decades = [...new Set(rows.map((r) => r.decade))];
    const series = d3.groups(rows, (r) => r.discipline);
    const W = Math.max(280, el.clientWidth), H = 250;
    const svg = d3.select(el).append('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    const endLabel = (s) => `${s[0]} ${pct(s[1][s[1].length - 1].share)}`;
    const right = d3.max(series, (s) => textWidth(svg.node(), endLabel(s))) + 12;
    const yMax = Math.ceil(d3.max(rows, (r) => r.share) * 10) / 10;
    const y = d3.scaleLinear([0, yMax], [H - 24, 8]);
    const leftM = textWidth(svg.node(), pct(yMax)) + 8;
    const x = d3.scalePoint(decades, [leftM + 6, W - right]);
    const ticks = y.ticks(4);
    svg.selectAll('line.grid').data(ticks).join('line').attr('x1', leftM).attr('x2', W - right).attr('y1', y).attr('y2', y).attr('stroke', 'var(--cds-chart-grid)');
    svg.selectAll('text.yt').data(ticks).join('text').attr('class', 'muted').attr('x', leftM - 6).attr('y', (d) => y(d) + 4).attr('text-anchor', 'end').text(pct);
    svg.selectAll('text.xt').data(decades).join('text').attr('class', 'muted').attr('x', (d) => x(d)).attr('y', H - 4).attr('text-anchor', 'middle')
      .text((d) => (x.step() < 52 ? d.replace(/^19(\d\d)–79$/, "'$1–79").replace(/^(\d\d)(\d\d)s$/, "'$2s") : d));
    const line = d3.line((r) => x(r.decade), (r) => y(r.share));
    // end labels, nudged apart so they never overlap
    const ends = series.map((s, i) => ({s, i, y: y(s[1][s[1].length - 1].share) + 4})).sort((a, b) => a.y - b.y);
    for (let k = 1; k < ends.length; k++) if (ends[k].y - ends[k - 1].y < 15) ends[k].y = ends[k - 1].y + 15;
    series.forEach(([name, pts], i) => {
      svg.append('path').attr('d', line(pts)).attr('fill', 'none').attr('stroke', dash.colors[i]).attr('stroke-width', 2).attr('stroke-linejoin', 'round').attr('stroke-linecap', 'round');
      svg.selectAll(null).data(pts).join('circle').attr('cx', (r) => x(r.decade)).attr('cy', (r) => y(r.share)).attr('r', 3).attr('fill', dash.colors[i]);
    });
    ends.forEach(({s, i, y: ly}) => svg.append('text').attr('x', W - right + 8).attr('y', ly).style('fill', dash.colors[i]).text(endLabel(s)));
    const tip = tipFor(el);
    svg.selectAll('rect.hover').data(decades).join('rect').attr('x', (d) => x(d) - x.step() / 2).attr('y', 0).attr('width', x.step()).attr('height', H).attr('fill', 'transparent')
      .on('mousemove', (e, d) => {
        const [mx, my] = d3.pointer(e, el);
        tip.show([['k', d], ...series.map(([name, pts]) => { const r = pts.find((p) => p.decade === d); return ['', `${name}: ${pct(r.share)} (${num(r.items)} of ${num(r.total)})`]; })], mx, my);
      })
      .on('mouseleave', () => tip.hide());
  });

  // Practice Points matrix
  dash.draw('pp-matrix', (el) => {
    if (!ok('articles')) return reset(el);
    const pps = dash.data('articles').data.filter((a) => a.pp_number).sort((a, b) => Number(a.pp_number) - Number(b.pp_number));
    el.replaceChildren();
    const R = [['mat', 'Materials'], ['doc', 'Documentation'], ['petc', 'Preservation eng.'], ['sp', 'Sustainable'], ['codes', 'Codes and standards'], ['mh', 'Modern heritage'], ['dis', 'Disaster (PETC)'], null, ['eng', 'Engineering'], ['arch', 'Architecture'], ['cons', 'Conservation']];
    const W = Math.max(280, el.clientWidth);
    const svg = d3.select(el).append('svg').attr('width', '100%');
    const left = d3.max(R.filter(Boolean), (r) => textWidth(svg.node(), r[1])) + 10;
    const cw = (W - left) / pps.length, rh = 20, top = 18, H = top + R.length * rh;
    svg.attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    const rad = Math.max(2.5, Math.min(6, cw / 2 - 1.5));
    R.forEach((r, ri) => {
      if (!r) return;
      const cy = top + ri * rh + rh / 2;
      svg.append('text').attr('x', 0).attr('y', cy + 4).attr('class', ri > 7 ? 'muted' : '').text(r[1]);
      svg.append('line').attr('x1', left).attr('x2', W).attr('y1', cy).attr('y2', cy).attr('stroke', 'var(--cds-chart-grid)');
      svg.selectAll(null).data(pps).join('circle').attr('cx', (_, i) => left + i * cw + cw / 2).attr('cy', cy).attr('r', rad)
        .attr('fill', (p) => (p[r[0]] === '1' ? dash.colors[ri > 7 ? 2 : 0] : 'var(--color-panel)'))
        .attr('stroke', (p) => (p[r[0]] === '1' ? 'none' : 'var(--cds-chart-grid)'));
    });
    const every = cw < 14 ? 5 : 1;
    svg.selectAll('text.n').data(pps).join('text').attr('class', 'n muted').attr('x', (_, i) => left + i * cw + cw / 2).attr('y', 11).attr('text-anchor', 'middle')
      .text((p, i) => (i === 0 || (i + 1) % every === 0 ? p.pp_number : ''));
    const tip = tipFor(el);
    svg.selectAll('rect.hover').data(pps).join('rect').attr('x', (_, i) => left + i * cw).attr('y', 0).attr('width', cw).attr('height', H).attr('fill', 'transparent')
      .on('mousemove', (e, p) => { const [mx, my] = d3.pointer(e, el); tip.show([['k', `Practice Point ${p.pp_number}, ${p.year}`], ['', p.title], ['k', p.authors]], mx, my); })
      .on('mouseleave', () => tip.hide());
  });

  // Table with committee filter and search
  const state = {filter: '', q: ''};
  const C_KEYS = ['doc', 'mat', 'petc', 'codes', 'mh', 'sp', 'dis'];
  const visible = () => {
    const rows = dash.data('articles').data;
    const q = state.q.trim().toLowerCase();
    return rows.filter((a) => {
      if (state.filter === 'none') { if (C_KEYS.some((k) => a[k] === '1')) return false; }
      else if (state.filter && a[state.filter] !== '1') return false;
      return !q || `${a.title} ${a.authors}`.toLowerCase().includes(q);
    }).sort((a, b) => Number(b.year) - Number(a.year) || d3.ascending(a.id, b.id));
  };
  document.querySelectorAll('#apt-filter').forEach((s) => s.addEventListener('change', () => { state.filter = s.value; dash.draw('table'); dash.draw('table-count'); }));
  document.querySelectorAll('#apt-search').forEach((s) => s.addEventListener('input', () => { state.q = s.value; dash.draw('table'); dash.draw('table-count'); }));

  dash.draw('table-count', (el) => { el.textContent = ok('articles') ? num(visible().length) : '—'; });
  dash.draw('table', (tb) => {
    if (!ok('articles') || !ok('item_tags')) { tb.replaceChildren(); return; }
    const tags = new Map(dash.data('item_tags').data.map((t) => [t.id, t]));
    tb.replaceChildren(...visible().map((a) => {
      const tr = document.createElement('tr'); tr.dataset.key = a.id;
      const t = tags.get(a.id) || {};
      [[a.year, 'num'], [a.pp_number, 'pp'], [a.title, ''], [a.authors, 'wide'], [t.committees, ''], [t.disciplines, 'wide']].forEach(([v, cls]) => {
        const td = document.createElement('td'); if (cls) td.className = cls; td.textContent = v || ''; tr.append(td);
      });
      return tr;
    }));
  });
