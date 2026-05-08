/**
 * Knowledge Graph Explorer
 * Force-directed graph visualization using D3.js v7
 */
(function() {
  'use strict';

  // ---- Config ----
  const COLORS = {
    palace: '#27ae60',
    emperor: '#c0392b',
    figure: '#3498db',
    event: '#e67e22'
  };

  const TYPE_LABELS = {
    palace: '宫殿',
    emperor: '皇帝',
    figure: '人物',
    event: '事件'
  };

  // ---- State ----
  let graphData = null;
  let nodes = [];
  let links = [];
  let nodeMap = {};
  let simulation = null;
  let svg = null;
  let g = null;
  let linkGroup, nodeGroup, labelGroup;
  let zoom;
  let showLabels = true;
  let activeFilters = { palace: true, emperor: true, figure: true, event: true };

  // ---- Init ----
  function init() {
    loadAllData();
    setupEventListeners();
  }

  function loadAllData() {
    const basePath = '../../data/';
    const datasets = ['palaces', 'emperors', 'figures', 'events', 'relations'];
    let loaded = 0;
    const results = {};

    datasets.forEach(function(name) {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', basePath + name + '.json');
      xhr.onload = function() {
        if (xhr.status === 200) {
          results[name] = JSON.parse(xhr.responseText);
        }
        loaded++;
        if (loaded === datasets.length) {
          buildGraph(results);
        }
      };
      xhr.onerror = function() {
        loaded++;
        if (loaded === datasets.length) {
          buildGraph(results);
        }
      };
      xhr.send();
    });
  }

  // ---- Build Graph ----
  function buildGraph(data) {
    nodes = [];
    links = [];
    nodeMap = {};

    // Add palaces
    if (data.palaces) {
      Object.keys(data.palaces).forEach(function(id) {
        var p = data.palaces[id];
        var node = {
          id: id,
          label: p.name,
          type: 'palace',
          category: p.category || '',
          description: p.description || '',
          built_year: p.built_year || null
        };
        nodes.push(node);
        nodeMap[id] = node;
      });
    }

    // Add emperors
    if (data.emperors) {
      Object.keys(data.emperors).forEach(function(id) {
        var e = data.emperors[id];
        var node = {
          id: id,
          label: e.name,
          type: 'emperor',
          era_name: e.era_name || '',
          dynasty: e.dynasty || '',
          description: e.description || '',
          reign_start: e.reign_start || null,
          reign_end: e.reign_end || null
        };
        nodes.push(node);
        nodeMap[id] = node;
      });
    }

    // Add figures
    if (data.figures) {
      Object.keys(data.figures).forEach(function(id) {
        var f = data.figures[id];
        var node = {
          id: id,
          label: f.name,
          type: 'figure',
          category: f.category || '',
          dynasty: f.dynasty || '',
          description: f.description || ''
        };
        nodes.push(node);
        nodeMap[id] = node;
      });
    }

    // Add events
    if (data.events) {
      Object.keys(data.events).forEach(function(id) {
        var ev = data.events[id];
        var node = {
          id: id,
          label: ev.name,
          type: 'event',
          category: ev.category || '',
          description: ev.description || '',
          start_year: ev.start_year || null,
          end_year: ev.end_year || null
        };
        nodes.push(node);
        nodeMap[id] = node;
      });
    }

    // Add relations as links
    if (data.relations && data.relations.relations) {
      data.relations.relations.forEach(function(r) {
        // Only include links where both nodes exist
        if (nodeMap[r.from] && nodeMap[r.to]) {
          links.push({
            source: r.from,
            target: r.to,
            type: r.type || '',
            period: r.period || '',
            note: r.note || ''
          });
        }
      });
    }

    // Subsample if too large for performance
    if (nodes.length > 300) {
      subsampleGraph(data);
    }

    renderGraph();
    updateStats();
  }

  function subsampleGraph(data) {
    // Keep all emperors and events, sample palaces and figures
    var emperors = nodes.filter(function(n) { return n.type === 'emperor'; });
    var events = nodes.filter(function(n) { return n.type === 'event'; });
    var palaces = nodes.filter(function(n) { return n.type === 'palace'; });
    var figures = nodes.filter(function(n) { return n.type === 'figure'; });

    // Keep key palaces (those with coordinates or built in 1420)
    var keyPalaces = palaces.filter(function(p) {
      return p.built_year === 1420 || nodeMap[p.id] && nodeMap[p.id].category === '外朝大殿' || nodeMap[p.id] && nodeMap[p.id].category === '内廷后寝';
    });

    // Keep figures connected to emperors
    var emperorIds = new Set(emperors.map(function(e) { return e.id; }));
    var connectedFigures = figures.filter(function(f) {
      return links.some(function(l) {
        return (l.source === f.id && emperorIds.has(l.target)) ||
               (l.target === f.id && emperorIds.has(l.source));
      });
    });

    // Limit figures to most connected
    var figureDegrees = connectedFigures.map(function(f) {
      return { node: f, degree: links.filter(function(l) { return l.source === f.id || l.target === f.id; }).length };
    });
    figureDegrees.sort(function(a, b) { return b.degree - a.degree; });

    nodes = emperors.concat(events).concat(keyPalaces);
    var maxFigures = 100;
    figureDegrees.slice(0, maxFigures).forEach(function(fd) { nodes.push(fd.node); });

    var nodeIds = new Set(nodes.map(function(n) { return n.id; }));
    links = links.filter(function(l) {
      return nodeIds.has(l.source) && nodeIds.has(l.target);
    });

    nodeMap = {};
    nodes.forEach(function(n) { nodeMap[n.id] = n; });
  }

  // ---- Render Graph ----
  function renderGraph() {
    var container = document.getElementById('graph-container');
    var width = container.clientWidth;
    var height = container.clientHeight;

    svg = d3.select('#graph-svg')
      .attr('width', width)
      .attr('height', height);

    svg.selectAll('*').remove();

    // Add zoom behavior
    zoom = d3.zoom()
      .scaleExtent([0.1, 5])
      .on('zoom', function(event) {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    // Main group
    g = svg.append('g');

    // Defs for arrow markers
    svg.append('defs').append('marker')
      .attr('id', 'arrowhead')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 28)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#484f58');

    // Groups for links and nodes
    linkGroup = g.append('g').attr('class', 'links');
    labelGroup = g.append('g').attr('class', 'link-labels');
    nodeGroup = g.append('g').attr('class', 'nodes');

    // Filter active nodes
    var activeNodes = nodes.filter(function(n) { return activeFilters[n.type]; });
    var activeNodeIds = new Set(activeNodes.map(function(n) { return n.id; }));
    var activeLinks = links.filter(function(l) {
      var src = typeof l.source === 'object' ? l.source.id : l.source;
      var tgt = typeof l.target === 'object' ? l.target.id : l.target;
      return activeNodeIds.has(src) && activeNodeIds.has(tgt);
    });

    // Create force simulation
    simulation = d3.forceSimulation(activeNodes)
      .force('link', d3.forceLink(activeLinks).id(function(d) { return d.id; }).distance(80))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(function(d) { return getNodeRadius(d) + 5; }))
      .force('x', d3.forceX(width / 2).strength(0.03))
      .force('y', d3.forceY(height / 2).strength(0.03));

    // Draw links
    var link = linkGroup.selectAll('.link')
      .data(activeLinks)
      .join('line')
      .attr('class', 'link')
      .attr('stroke', '#484f58')
      .attr('stroke-width', 1.5);

    // Draw link labels
    var linkLabel = labelGroup.selectAll('.link-label')
      .data(activeLinks)
      .join('text')
      .attr('class', 'link-label')
      .text(function(d) { return d.type || ''; });

    // Draw nodes
    var node = nodeGroup.selectAll('.node')
      .data(activeNodes)
      .join('g')
      .attr('class', 'node')
      .call(d3.drag()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded));

    // Node circles
    node.append('circle')
      .attr('class', 'node-circle')
      .attr('r', function(d) { return getNodeRadius(d); })
      .attr('fill', function(d) { return COLORS[d.type] || '#888'; });

    // Node labels
    node.append('text')
      .attr('class', 'node-label')
      .attr('dy', function(d) { return getNodeRadius(d) + 14; })
      .text(function(d) {
        return d.label.length > 8 ? d.label.substring(0, 8) + '…' : d.label;
      })
      .style('display', showLabels ? 'block' : 'none');

    // Node interactions
    node.on('mouseenter', handleMouseEnter)
        .on('mousemove', handleMouseMove)
        .on('mouseleave', handleMouseLeave)
        .on('click', handleClick);

    // Tick handler
    simulation.on('tick', function() {
      link
        .attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.y; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.y; });

      linkLabel
        .attr('x', function(d) { return (d.source.x + d.target.x) / 2; })
        .attr('y', function(d) { return (d.source.y + d.target.y) / 2 - 4; });

      node.attr('transform', function(d) {
        return 'translate(' + d.x + ',' + d.y + ')';
      });
    });

    // Store references for filtering
    simulation._nodeSelection = node;
    simulation._linkSelection = link;
    simulation._linkLabelSelection = linkLabel;
    simulation._activeNodes = activeNodes;
    simulation._activeLinks = activeLinks;
  }

  function getNodeRadius(d) {
    switch (d.type) {
      case 'emperor': return 18;
      case 'palace': return 15;
      case 'event': return 12;
      case 'figure': return 10;
      default: return 12;
    }
  }

  // ---- Drag Handlers ----
  function dragStarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragEnded(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  // ---- Interaction Handlers ----
  function handleMouseEnter(event, d) {
    highlightNode(d);
    showTooltip(event, d);
  }

  function handleMouseMove(event, d) {
    moveTooltip(event);
  }

  function handleMouseLeave(event, d) {
    resetHighlight();
    hideTooltip();
  }

  function handleClick(event, d) {
    showNodeDetail(d);
  }

  function highlightNode(d) {
    var node = simulation._nodeSelection;
    var link = simulation._linkSelection;
    var linkLabel = simulation._linkLabelSelection;

    if (!node || !link) return;

    var connectedIds = new Set();
    connectedIds.add(d.id);

    simulation._activeLinks.forEach(function(l) {
      var src = typeof l.source === 'object' ? l.source.id : l.source;
      var tgt = typeof l.target === 'object' ? l.target.id : l.target;
      if (src === d.id) connectedIds.add(tgt);
      if (tgt === d.id) connectedIds.add(src);
    });

    node.select('.node-circle')
      .classed('highlighted', function(n) { return n.id === d.id; })
      .classed('dimmed', function(n) { return !connectedIds.has(n.id); });

    node.select('.node-label')
      .classed('dimmed', function(n) { return !connectedIds.has(n.id); });

    link.classed('dimmed', function(l) {
      var src = typeof l.source === 'object' ? l.source.id : l.source;
      var tgt = typeof l.target === 'object' ? l.target.id : l.target;
      return !(src === d.id || tgt === d.id);
    });

    linkLabel.classed('dimmed', function(l) {
      var src = typeof l.source === 'object' ? l.source.id : l.source;
      var tgt = typeof l.target === 'object' ? l.target.id : l.target;
      return !(src === d.id || tgt === d.id);
    });
  }

  function resetHighlight() {
    var node = simulation._nodeSelection;
    var link = simulation._linkSelection;
    var linkLabel = simulation._linkLabelSelection;

    if (!node) return;

    node.select('.node-circle').classed('highlighted', false).classed('dimmed', false);
    node.select('.node-label').classed('dimmed', false);
    if (link) link.classed('dimmed', false);
    if (linkLabel) linkLabel.classed('dimmed', false);
  }

  // ---- Tooltip ----
  function showTooltip(event, d) {
    var tooltip = document.getElementById('tooltip');
    tooltip.innerHTML =
      '<div class="tt-name">' + d.label + '</div>' +
      '<div class="tt-type">' + TYPE_LABELS[d.type] + (d.dynasty ? ' · ' + d.dynasty + '朝' : '') +
      (d.category ? ' · ' + d.category : '') + '</div>';
    tooltip.classList.add('visible');
    moveTooltip(event);
  }

  function moveTooltip(event) {
    var tooltip = document.getElementById('tooltip');
    var x = event.clientX + 15;
    var y = event.clientY + 15;
    if (x + 250 > window.innerWidth) x = event.clientX - 260;
    if (y + 60 > window.innerHeight) y = event.clientY - 60;
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
  }

  function hideTooltip() {
    document.getElementById('tooltip').classList.remove('visible');
  }

  // ---- Node Detail Panel ----
  function showNodeDetail(d) {
    var panel = document.getElementById('node-detail');
    var content = document.getElementById('detail-content');
    var color = COLORS[d.type] || '#888';

    var meta = '';
    if (d.era_name) meta += '<p><strong>年号:</strong> ' + d.era_name + '</p>';
    if (d.dynasty) meta += '<p><strong>朝代:</strong> ' + d.dynasty + '朝</p>';
    if (d.reign_start) meta += '<p><strong>在位:</strong> ' + d.reign_start + ' — ' + (d.reign_end || '?') + '</p>';
    if (d.built_year) meta += '<p><strong>始建:</strong> ' + d.built_year + '年</p>';
    if (d.start_year) meta += '<p><strong>时间:</strong> ' + d.start_year + (d.end_year && d.end_year !== d.start_year ? ' — ' + d.end_year : '') + '</p>';
    if (d.category) meta += '<p><strong>类别:</strong> ' + d.category + '</p>';

    // Find connections
    var connections = [];
    simulation._activeLinks.forEach(function(l) {
      var src = typeof l.source === 'object' ? l.source.id : l.source;
      var tgt = typeof l.target === 'object' ? l.target.id : l.target;
      if (src === d.id) {
        var targetNode = nodeMap[tgt];
        if (targetNode) connections.push(targetNode.label + ' (' + l.type + ')');
      }
      if (tgt === d.id) {
        var sourceNode = nodeMap[src];
        if (sourceNode) connections.push(sourceNode.label + ' (' + l.type + ')');
      }
    });

    var connectionsHTML = '';
    if (connections.length > 0) {
      connectionsHTML = '<div class="connections"><h4>关联 (' + connections.length + ')</h4><ul>';
      connections.slice(0, 15).forEach(function(c) {
        connectionsHTML += '<li>' + c + '</li>';
      });
      if (connections.length > 15) {
        connectionsHTML += '<li>... 还有 ' + (connections.length - 15) + ' 个关联</li>';
      }
      connectionsHTML += '</ul></div>';
    }

    // Wiki link
    var wikiLink = '';
    if (d.type === 'emperor') {
      wikiLink = '<a class="wiki-link" href="../../docs/emperors/' + d.id + '.html">📖 查看 Emperor Wiki</a>';
    } else if (d.type === 'palace') {
      wikiLink = '<a class="wiki-link" href="../../docs/palaces/' + d.id + '.html">📖 查看 Palace Wiki</a>';
    }

    content.innerHTML =
      '<h3 style="color:' + color + '">' + d.label + '</h3>' +
      meta +
      '<p>' + (d.description || '') + '</p>' +
      connectionsHTML +
      wikiLink;

    panel.classList.add('visible');
  }

  // ---- Filters ----
  function applyFilters() {
    activeFilters = {};
    document.querySelectorAll('.filter-label input[type="checkbox"]').forEach(function(cb) {
      activeFilters[cb.dataset.type] = cb.checked;
    });
    if (simulation) {
      simulation.stop();
      renderGraph();
      updateStats();
    }
  }

  function updateStats() {
    var stats = document.getElementById('graph-stats');
    var typeCounts = {};
    nodes.forEach(function(n) {
      if (activeFilters[n.type]) {
        typeCounts[n.type] = (typeCounts[n.type] || 0) + 1;
      }
    });
    var activeLinkCount = simulation && simulation._activeLinks ? simulation._activeLinks.length : 0;

    var html = '';
    Object.keys(TYPE_LABELS).forEach(function(type) {
      if (activeFilters[type]) {
        html += '<div>' + TYPE_LABELS[type] + ': ' + (typeCounts[type] || 0) + '</div>';
      }
    });
    html += '<div>关系: ' + activeLinkCount + '</div>';
    stats.innerHTML = html;
  }

  // ---- Search ----
  function searchNode(query) {
    if (!query || !simulation) return;
    query = query.toLowerCase().trim();

    var found = nodes.filter(function(n) {
      return n.label.toLowerCase().indexOf(query) !== -1 ||
             (n.era_name && n.era_name.toLowerCase().indexOf(query) !== -1) ||
             n.id.toLowerCase().indexOf(query) !== -1;
    });

    if (found.length === 0) return;

    var target = found[0];

    // Zoom to node
    if (target.x !== undefined) {
      var container = document.getElementById('graph-container');
      var width = container.clientWidth;
      var height = container.clientHeight;

      svg.transition().duration(750).call(
        zoom.transform,
        d3.zoomIdentity.translate(width / 2 - target.x * 2, height / 2 - target.y * 2).scale(2)
      );
    }

    // Highlight and show detail
    highlightNode(target);
    showNodeDetail(target);

    // Clear highlight after delay
    setTimeout(function() { resetHighlight(); }, 3000);
  }

  // ---- Event Listeners ----
  function setupEventListeners() {
    // Search
    var searchInput = document.getElementById('search-input');
    var searchBtn = document.getElementById('search-btn');
    var clearBtn = document.getElementById('clear-btn');

    searchBtn.addEventListener('click', function() {
      searchNode(searchInput.value);
    });

    searchInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') searchNode(searchInput.value);
    });

    clearBtn.addEventListener('click', function() {
      searchInput.value = '';
      resetHighlight();
      document.getElementById('node-detail').classList.remove('visible');
      svg.transition().duration(500).call(
        zoom.transform,
        d3.zoomIdentity
      );
    });

    // Filters
    document.querySelectorAll('.filter-label input[type="checkbox"]').forEach(function(cb) {
      cb.addEventListener('change', applyFilters);
    });

    // Reset zoom
    document.getElementById('reset-zoom').addEventListener('click', function() {
      var container = document.getElementById('graph-container');
      svg.transition().duration(500).call(
        zoom.transform,
        d3.zoomIdentity
      );
    });

    // Toggle labels
    document.getElementById('toggle-labels').addEventListener('click', function() {
      showLabels = !showLabels;
      d3.selectAll('.node-label').style('display', showLabels ? 'block' : 'none');
      d3.selectAll('.link-label').style('display', showLabels ? 'block' : 'none');
    });

    // Close detail
    document.getElementById('detail-close').addEventListener('click', function() {
      document.getElementById('node-detail').classList.remove('visible');
    });

    // Close detail on overlay click
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        document.getElementById('node-detail').classList.remove('visible');
      }
    });

    // Resize handler
    window.addEventListener('resize', function() {
      if (simulation) {
        var container = document.getElementById('graph-container');
        simulation.force('center', d3.forceCenter(container.clientWidth / 2, container.clientHeight / 2));
        svg.attr('width', container.clientWidth).attr('height', container.clientHeight);
        simulation.alpha(0.3).restart();
      }
    });
  }

  // ---- Start ----
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
