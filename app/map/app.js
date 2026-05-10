(function() {
  const svg = document.getElementById('palace-map');
  const palaceLayer = document.getElementById('palace-layer');
  const labelLayer = document.getElementById('label-layer');
  const sidebarContent = document.getElementById('sidebar-content');
  const yearSlider = document.getElementById('year-slider');
  const yearDisplay = document.getElementById('year-display');
  const dynastyDisplay = document.getElementById('dynasty-display');

  let selectedPalace = null;

  // Render palace rectangles
  function renderPalaces(filterYear) {
    palaceLayer.innerHTML = '';
    labelLayer.innerHTML = '';

    Object.values(PALACES).forEach(palace => {
      // Check if palace existed at the filtered year
      if (filterYear && palace.built_year > filterYear) return;

      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', palace.coordinates.x - palace.width / 2);
      rect.setAttribute('y', palace.coordinates.y - palace.height / 2);
      rect.setAttribute('width', palace.width);
      rect.setAttribute('height', palace.height);
      rect.setAttribute('fill', palace.color || '#d4a017');
      rect.setAttribute('rx', '4');
      rect.setAttribute('class', 'palace-rect');
      rect.setAttribute('data-id', palace.id);

      rect.addEventListener('click', () => selectPalace(palace.id));
      palaceLayer.appendChild(rect);

      // Label - only for important buildings, smaller text for gates/doors
      const noLabelCats = ['门禁', '前朝门禁', '内廷门禁', '外朝门禁'];
      const isMinor = palace.category in noLabelCats;
      
      if (!isMinor || palace.width >= 60) {
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', palace.coordinates.x);
        text.setAttribute('y', palace.coordinates.y - 2);
        text.setAttribute('class', 'palace-label');
        // Smaller text for minor buildings
        if (isMinor) {
          text.setAttribute('font-size', '10');
          text.setAttribute('fill', '#aaa');
        }
        text.textContent = palace.name;
        labelLayer.appendChild(text);

        // Alias (only for important buildings)
        if (palace.aliases && palace.aliases.length > 0 && !isMinor) {
          const alias = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          alias.setAttribute('x', palace.coordinates.x);
          alias.setAttribute('y', palace.coordinates.y + 14);
          alias.setAttribute('class', 'palace-alias');
          alias.textContent = palace.aliases[0];
          labelLayer.appendChild(alias);
        }
      }
    });
  }

  // Select a palace and show details
  function selectPalace(palaceId) {
    const palace = PALACES[palaceId];
    if (!palace) return;

    selectedPalace = palaceId;

    // Update selection state
    document.querySelectorAll('.palace-rect').forEach(el => {
      el.classList.toggle('selected', el.dataset.id === palaceId);
    });

    const rels = PALACE_RELATIONS[palaceId] || { persons: [], events: [] };

    let html = `<div class="palace-detail">`;
    html += `<h2>${palace.name}</h2>`;
    if (palace.aliases && palace.aliases.length > 0) {
      html += `<div class="aliases">又名：${palace.aliases.join('、')}</div>`;
    }
    html += `<div class="info-grid">
      <span class="info-label">类别</span><span class="info-value">${palace.category}</span>
      <span class="info-label">始建</span><span class="info-value">${palace.built_year}年</span>
      <span class="info-label">朝代</span><span class="info-value">${palace.dynasty}</span>`;

    if (palace.dimensions && palace.dimensions.width_m) {
      html += `<span class="info-label">尺寸</span><span class="info-value">${palace.dimensions.width_m}m x ${palace.dimensions.depth_m}m, 高${palace.dimensions.height_m}m</span>`;
    }
    html += `</div>`;

    html += `<div class="description">${palace.description}</div>`;

    if (palace.significance) {
      html += `<div style="color:#d4a017;font-size:13px;margin-bottom:12px;">★ ${palace.significance}</div>`;
    }

    // Related persons
    if (rels.persons.length > 0) {
      html += `<div class="section-title">相关人物 (${rels.persons.length})</div>`;
      rels.persons.forEach(p => {
        const person = ALL_PERSONS[p.id];
        const birthDeath = person && person.birth_year ?
          `${person.birth_year}-${person.death_year || '?'}` : '';
        html += `<div class="relation-item">
          <span class="type-badge">${p.type}</span>
          <div class="details">
            <div class="name">${p.name} ${birthDeath}</div>
            ${p.period ? `<div class="note">时期：${p.period}</div>` : ''}
            ${p.note ? `<div class="note">${p.note}</div>` : ''}
          </div>
        </div>`;
      });
    }

    // Related events
    if (rels.events.length > 0) {
      html += `<div class="section-title">相关事件 (${rels.events.length})</div>`;
      rels.events.forEach(e => {
        html += `<div class="event-item">
          <div class="event-name">${e.name}</div>
          <div class="event-desc">${e.description}</div>
          <div class="event-year">${e.year}年</div>
        </div>`;
      });
    }

    html += `</div>`;
    sidebarContent.innerHTML = html;
  }

  // Time slider
  function getDynastyInfo(year) {
    if (year < 1644) {
      if (year >= 1402 && year < 1425) return '明·永乐/洪熙';
      if (year >= 1425 && year < 1521) return '明·宣德-正德';
      if (year >= 1521 && year < 1567) return '明·嘉靖';
      if (year >= 1567 && year < 1620) return '明·隆庆/万历';
      if (year >= 1620 && year < 1627) return '明·泰昌/天启';
      if (year >= 1627 && year < 1644) return '明·崇祯';
      return '明';
    } else {
      if (year >= 1644 && year < 1662) return '清·顺治';
      if (year >= 1662 && year < 1722) return '清·康熙';
      if (year >= 1722 && year < 1735) return '清·雍正';
      if (year >= 1735 && year < 1796) return '清·乾隆';
      if (year >= 1796 && year < 1820) return '清·嘉庆';
      if (year >= 1820 && year < 1850) return '清·道光';
      if (year >= 1850 && year < 1861) return '清·咸丰';
      if (year >= 1861 && year < 1875) return '清·同治';
      if (year >= 1875 && year < 1908) return '清·光绪';
      if (year >= 1908 && year < 1912) return '清·宣统';
      if (year >= 1912 && year < 1924) return '逊帝居宫';
      return '故宫博物院';
    }
  }

  yearSlider.addEventListener('input', function() {
    const year = parseInt(this.value);
    yearDisplay.textContent = year + '年';
    dynastyDisplay.textContent = '（' + getDynastyInfo(year) + '）';
    renderPalaces(year);
    if (selectedPalace && PALACES[selectedPalace]) {
      selectPalace(selectedPalace);
    }
  });

  // Initial render
  renderPalaces(parseInt(yearSlider.value));
})();
