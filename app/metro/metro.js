/**
 * 皇帝地铁图 — Emperor Metro Timeline
 * Interactive subway-map-style timeline of Ming and Qing emperors
 */
(function() {
  'use strict';

  // ---- Config ----
  const CONFIG = {
    mingColor: '#c0392b',
    qingColor: '#c9a227',
    eventColor: '#e67e22',
    bgColor: '#0d1117',
    stationSpacing: 85,
    mingLineY: 120,
    qingLineY: 260,
    connectorX: 0,
    paddingX: 60,
    paddingY: 50,
    stationTopOffset: -40,
    stationBottomOffset: 30
  };

  // ---- State ----
  let data = null;
  let svgWidth = 0;
  let zoomLevel = 1;

  // ---- Init ----
  function init() {
    loadData();
    setupControls();
  }

  function loadData() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'data/metro_data.json');
    xhr.onload = function() {
      if (xhr.status === 200) {
        data = JSON.parse(xhr.responseText);
        renderMetro();
      }
    };
    xhr.send();
  }

  // ---- Rendering ----
  function renderMetro() {
    const svg = document.getElementById('metro-svg');
    const mingEmperors = data.ming_emperors;
    const qingEmperors = data.qing_emperors;

    const totalStations = Math.max(mingEmperors.length, qingEmperors.length);
    svgWidth = CONFIG.paddingX * 2 + (totalStations - 1) * CONFIG.stationSpacing + 100;

    svg.setAttribute('width', svgWidth);
    svg.setAttribute('height', '420');
    svg.innerHTML = '';

    // Draw year axis
    drawYearAxis(svg);

    // Draw Ming line
    drawLine(svg, mingEmperors, CONFIG.mingLineY, 'ming', CONFIG.mingColor);

    // Draw Qing line
    drawLine(svg, qingEmperors, CONFIG.qingLineY, 'qing', CONFIG.qingColor);

    // Draw connector between lines
    drawConnector(svg, mingEmperors, qingEmperors);

    // Draw dynasty labels
    drawDynastyLabels(svg);

    // Draw events
    drawEvents(svg);
  }

  function yearToX(year) {
    const yearRange = data.year_range.max - data.year_range.min;
    const usableWidth = svgWidth - CONFIG.paddingX * 2;
    return CONFIG.paddingX + ((year - data.year_range.min) / yearRange) * usableWidth;
  }

  function drawYearAxis(svg) {
    const ns = 'http://www.w3.org/2000/svg';
    const minY = 370;
    const maxY = 400;

    for (let year = 1370; year <= 1910; year += 10) {
      const x = yearToX(year);

      const tick = document.createElementNS(ns, 'line');
      tick.setAttribute('x1', x);
      tick.setAttribute('y1', minY);
      tick.setAttribute('x2', x);
      tick.setAttribute('y2', maxY);
      tick.setAttribute('class', 'year-tick');
      svg.appendChild(tick);

      if (year % 50 === 0) {
        const label = document.createElementNS(ns, 'text');
        label.setAttribute('x', x);
        label.setAttribute('y', maxY + 15);
        label.setAttribute('text-anchor', 'middle');
        label.setAttribute('class', 'year-label');
        label.textContent = year;
        svg.appendChild(label);
      }
    }
  }

  function drawLine(svg, emperors, lineY, dynasty, color) {
    const ns = 'http://www.w3.org/2000/svg';

    // Draw the line
    if (emperors.length > 1) {
      const path = document.createElementNS(ns, 'path');
      let d = `M ${yearToX(emperors[0].reign_start)} ${lineY}`;

      for (let i = 0; i < emperors.length; i++) {
        const emp = emperors[i];
        const startX = yearToX(emp.reign_start);
        const endX = yearToX(emp.reign_end);

        if (i === 0) {
          d = `M ${startX} ${lineY} L ${endX} ${lineY}`;
        } else {
          d += ` M ${startX} ${lineY} L ${endX} ${lineY}`;
        }
      }
      path.setAttribute('d', d);
      path.setAttribute('class', `metro-line ${dynasty}`);
      svg.appendChild(path);

      // Draw reign segments with proportional width
      for (let i = 0; i < emperors.length; i++) {
        const emp = emperors[i];
        const x = yearToX(emp.reign_start);
        const xEnd = yearToX(emp.reign_end);
        const width = Math.max(xEnd - x, 2);

        // Reign segment bar
        const rect = document.createElementNS(ns, 'rect');
        rect.setAttribute('x', x);
        rect.setAttribute('y', lineY - 3);
        rect.setAttribute('width', width);
        rect.setAttribute('height', 6);
        rect.setAttribute('fill', color);
        rect.setAttribute('opacity', '0.3');
        rect.setAttribute('rx', '3');
        svg.insertBefore(rect, svg.lastChild);
      }
    }

    // Draw stations
    emperors.forEach(function(emp) {
      const group = document.createElementNS(ns, 'g');
      group.setAttribute('class', 'station-group');
      group.setAttribute('data-id', emp.id);

      const reignLength = emp.reign_end - emp.reign_start;
      let sizeClass = 'normal-reign';
      if (reignLength >= 40) sizeClass = 'long-reign';
      else if (reignLength <= 2) sizeClass = 'short-reign';

      const x = yearToX(emp.reign_start);

      // Station circle
      const circle = document.createElementNS(ns, 'circle');
      circle.setAttribute('cx', x);
      circle.setAttribute('cy', lineY);
      circle.setAttribute('r', sizeClass === 'long-reign' ? 16 : sizeClass === 'short-reign' ? 10 : 13);
      circle.setAttribute('class', `station-circle ${dynasty} ${sizeClass}`);
      group.appendChild(circle);

      // Inner circle for transfer-style look
      const inner = document.createElementNS(ns, 'circle');
      inner.setAttribute('cx', x);
      inner.setAttribute('cy', lineY);
      inner.setAttribute('r', sizeClass === 'long-reign' ? 8 : sizeClass === 'short-reign' ? 4 : 6);
      inner.setAttribute('fill', '#0d1117');
      inner.setAttribute('pointer-events', 'none');
      group.appendChild(inner);

      // Era name label
      const label = document.createElementNS(ns, 'text');
      label.setAttribute('x', x);
      label.setAttribute('y', lineY + CONFIG.stationTopOffset);
      label.setAttribute('text-anchor', 'middle');
      label.setAttribute('class', 'station-label');
      label.textContent = emp.era_name;
      group.appendChild(label);

      // Reign years
      const years = document.createElementNS(ns, 'text');
      years.setAttribute('x', x);
      years.setAttribute('y', lineY + CONFIG.stationBottomOffset);
      years.setAttribute('text-anchor', 'middle');
      years.setAttribute('class', 'station-years');
      years.textContent = emp.reign_start + (emp.reign_start !== emp.reign_end ? '-' + emp.reign_end : '');
      group.appendChild(years);

      // Events
      group.addEventListener('mouseenter', function(e) { showTooltip(e, emp, dynasty); });
      group.addEventListener('mousemove', function(e) { moveTooltip(e); });
      group.addEventListener('mouseleave', hideTooltip);
      group.addEventListener('click', function() { openModal(emp, dynasty); });

      svg.appendChild(group);
    });
  }

  function drawConnector(svg, mingEmps, qingEmps) {
    const ns = 'http://www.w3.org/2000/svg';

    // Connector from Chongzhen (last Ming) to Shunzhi (first Qing who entered Beijing)
    const chongzhen = mingEmps.find(function(e) { return e.id === 'chongzhen'; });
    const shunzhi = qingEmps.find(function(e) { return e.id === 'shunzhi'; });

    if (chongzhen && shunzhi) {
      const x1 = yearToX(chongzhen.reign_end);
      const x2 = yearToX(shunzhi.reign_start);
      const y1 = CONFIG.mingLineY;
      const y2 = CONFIG.qingLineY;

      const path = document.createElementNS(ns, 'path');
      path.setAttribute('d', `M ${x1} ${y1} L ${x2} ${y2}`);
      path.setAttribute('class', 'connector-line');
      svg.insertBefore(path, svg.firstChild.nextSibling);

      // Transfer station label
      const label = document.createElementNS(ns, 'text');
      label.setAttribute('x', (x1 + x2) / 2);
      label.setAttribute('y', (y1 + y2) / 2 + 4);
      label.setAttribute('text-anchor', 'middle');
      label.setAttribute('fill', '#8b949e');
      label.setAttribute('font-size', '9');
      label.setAttribute('font-family', '"PingFang SC", "Microsoft YaHei", sans-serif');
      label.textContent = '1644 鼎革';
      svg.insertBefore(label, svg.firstChild.nextSibling.nextSibling);
    }
  }

  function drawDynastyLabels(svg) {
    const ns = 'http://www.w3.org/2000/svg';

    // Ming label
    const mingLabel = document.createElementNS(ns, 'text');
    mingLabel.setAttribute('x', CONFIG.paddingX - 10);
    mingLabel.setAttribute('y', CONFIG.mingLineY + 5);
    mingLabel.setAttribute('text-anchor', 'end');
    mingLabel.setAttribute('class', 'dynasty-label ming');
    mingLabel.textContent = '明';
    svg.appendChild(mingLabel);

    // Qing label
    const qingLabel = document.createElementNS(ns, 'text');
    qingLabel.setAttribute('x', CONFIG.paddingX - 10);
    qingLabel.setAttribute('y', CONFIG.qingLineY + 5);
    qingLabel.setAttribute('text-anchor', 'end');
    qingLabel.setAttribute('class', 'dynasty-label qing');
    qingLabel.textContent = '清';
    svg.appendChild(qingLabel);
  }

  function drawEvents(svg) {
    const ns = 'http://www.w3.org/2000/svg';

    // Filter to important events only (those involving emperors)
    const importantCategories = ['政变', '战争', '修建工程', '文化工程', '逝世葬礼'];
    const keyEvents = data.timeline_events.filter(function(evt) {
      return importantCategories.indexOf(evt.category) !== -1;
    });

    // Limit to avoid clutter - show at most 20
    const shown = keyEvents.slice(0, 20);

    shown.forEach(function(evt) {
      const x = yearToX(evt.year);
      const y = CONFIG.qingLineY + 70;

      // Diamond marker
      const marker = document.createElementNS(ns, 'polygon');
      const size = 5;
      marker.setAttribute('points',
        `${x},${y - size} ${x + size},${y} ${x},${y + size} ${x - size},${y}`
      );
      marker.setAttribute('class', 'event-marker');
      marker.setAttribute('data-event-id', evt.id);

      marker.addEventListener('mouseenter', function(e) {
        showEventTooltip(e, evt);
      });
      marker.addEventListener('mousemove', function(e) { moveTooltip(e); });
      marker.addEventListener('mouseleave', hideTooltip);

      svg.appendChild(marker);

      // Event label (rotate some to avoid overlap)
      const label = document.createElementNS(ns, 'text');
      label.setAttribute('x', x);
      label.setAttribute('y', y + 18);
      label.setAttribute('text-anchor', 'middle');
      label.setAttribute('class', 'event-label');
      label.textContent = evt.name.substring(0, 8);
      svg.appendChild(label);
    });
  }

  // ---- Tooltip ----
  function showTooltip(e, emp, dynasty) {
    const tooltip = document.getElementById('tooltip');
    const reignLength = emp.reign_end - emp.reign_start;
    const color = dynasty === 'ming' ? CONFIG.mingColor : CONFIG.qingColor;

    tooltip.innerHTML =
      '<h4>' + emp.name + '</h4>' +
      '<p><span class="era">' + emp.era_name + '</span> · ' + dynasty + '朝</p>' +
      '<p>在位: ' + emp.reign_start + ' — ' + emp.reign_end +
        ' (' + reignLength + '年)</p>' +
      '<p>' + emp.description.substring(0, 80) + '...</p>';

    tooltip.style.borderColor = color;
    tooltip.classList.add('visible');
    moveTooltip(e);
  }

  function showEventTooltip(e, evt) {
    const tooltip = document.getElementById('tooltip');
    tooltip.innerHTML =
      '<h4>' + evt.name + '</h4>' +
      '<p>年份: ' + evt.year + '</p>' +
      '<p>类型: ' + evt.category + '</p>';
    tooltip.style.borderColor = CONFIG.eventColor;
    tooltip.classList.add('visible');
    moveTooltip(e);
  }

  function moveTooltip(e) {
    const tooltip = document.getElementById('tooltip');
    let x = e.clientX + 15;
    let y = e.clientY + 15;

    if (x + 320 > window.innerWidth) x = e.clientX - 330;
    if (y + 200 > window.innerHeight) y = e.clientY - 200;

    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
  }

  function hideTooltip() {
    document.getElementById('tooltip').classList.remove('visible');
  }

  // ---- Modal ----
  function openModal(emp, dynasty) {
    const overlay = document.getElementById('modal-overlay');
    const content = document.getElementById('modal-content');
    const color = dynasty === 'ming' ? CONFIG.mingColor : CONFIG.qingColor;

    let achievementsHTML = '';
    if (emp.achievements && emp.achievements.length > 0) {
      achievementsHTML = '<ul class="achievements">';
      emp.achievements.forEach(function(a) {
        achievementsHTML += '<li>' + a + '</li>';
      });
      achievementsHTML += '</ul>';
    }

    content.innerHTML =
      '<h2 style="color:' + color + '">' + emp.name + '</h2>' +
      '<p><strong>年号:</strong> ' + emp.era_name + ' · ' + dynasty + '朝</p>' +
      '<p><strong>在位:</strong> ' + emp.reign_start + ' — ' + emp.reign_end + '</p>' +
      '<p>' + emp.description + '</p>' +
      achievementsHTML +
      '<a class="wiki-link" href="../../docs/emperors/' + emp.id + '.html" target="_blank">📖 查看完整 Wiki 页面</a>';

    overlay.classList.add('visible');
  }

  // ---- Controls ----
  function setupControls() {
    // Modal close
    document.getElementById('modal-close').addEventListener('click', function() {
      document.getElementById('modal-overlay').classList.remove('visible');
    });

    document.getElementById('modal-overlay').addEventListener('click', function(e) {
      if (e.target === this) this.classList.remove('visible');
    });

    // Year slider
    var slider = document.getElementById('year-slider');
    var yearDisplay = document.getElementById('year-display');
    slider.addEventListener('input', function() {
      yearDisplay.textContent = '1368 — ' + this.value;
      // Could add filtering logic here
    });

    // Drag to scroll
    var scrollContainer = document.getElementById('metro-scroll');
    var isDown = false;
    var startX;
    var scrollLeft;

    scrollContainer.addEventListener('mousedown', function(e) {
      isDown = true;
      startX = e.pageX - scrollContainer.offsetLeft;
      scrollLeft = scrollContainer.scrollLeft;
    });

    scrollContainer.addEventListener('mouseleave', function() { isDown = false; });
    scrollContainer.addEventListener('mouseup', function() { isDown = false; });

    scrollContainer.addEventListener('mousemove', function(e) {
      if (!isDown) return;
      e.preventDefault();
      var x = e.pageX - scrollContainer.offsetLeft;
      var walk = (x - startX) * 2;
      scrollContainer.scrollLeft = scrollLeft - walk;
    });

    // Zoom buttons
    document.getElementById('zoom-in').addEventListener('click', function() {
      zoomLevel = Math.min(zoomLevel + 0.2, 2.5);
      applyZoom();
    });

    document.getElementById('zoom-out').addEventListener('click', function() {
      zoomLevel = Math.max(zoomLevel - 0.2, 0.5);
      applyZoom();
    });

    document.getElementById('reset-view').addEventListener('click', function() {
      zoomLevel = 1;
      applyZoom();
      scrollContainer.scrollLeft = 0;
    });

    // Scroll to start on load
    setTimeout(function() {
      scrollContainer.scrollLeft = 0;
    }, 100);
  }

  function applyZoom() {
    var svg = document.getElementById('metro-svg');
    svg.style.transform = 'scale(' + zoomLevel + ')';
    svg.style.transformOrigin = 'top left';
  }

  // ---- Keyboard ----
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      document.getElementById('modal-overlay').classList.remove('visible');
    }
  });

  // Start
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
