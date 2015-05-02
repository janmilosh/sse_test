$(function() {

  var width = 1000,
      height = 600,
      circleSmall,
      circleLarge,
      pathWidth = 0.25,
      initialFillColor = 'yellow',
      fadeOutFillColor = 'limegreen'    

  var evtSrc = new EventSource("/subscribe");
  
  evtSrc.onmessage = function(e) {
    var data = JSON.parse(e.data);
    try {
      addPointsToMap([[data.lat, data.lon]]);
    } catch(e) {
      console.log(e)
    }
  };

  setSizes();

  function setSizes() {
    var windowHeight = $(window).height();
    var windowWidth = $(window).width();
    if (windowWidth >= 1024) {
      width = windowWidth * 0.9;
    } else {
      width = 1000;
    }
    height = width * 0.6;
    circleSmall = 15 * width/1000;
    circleLarge = circleSmall * 10;
    strokeWidth = 1;

    $('#usa-map').css({'height': height + 'px',
                       'width': width + 'px',
                       'margin-left': 'auto',
                       'margin-right': 'auto',
                       'margin-top': ((windowHeight-height)/2) + 'px'
                     });
  }

  var projection = d3.geo.albersUsa()
    .scale(width * 1.2)
    .translate([width / 2, height / 2]);

  var path = d3.geo.path()
    .projection(projection);

  var svgSelection = d3.select("#usa-map")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  svgSelection.append("rect")
    .attr("class", "background")
    .attr("width", width)
    .attr("height", height);

  var group = svgSelection.append("g");

  var us = mapPath;

  group.selectAll("path")
    .data(topojson.feature(us, us.objects.states).features)
    .enter().append("path")
    .attr("d", path)
    .attr("class", "feature");

  group.append("path")
    .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
    .attr("class", "mesh")
    .attr("stroke-width", strokeWidth)
    .attr("d", path);

  function addPointsToMap(data) {
    circles = svgSelection.selectAll("circle")
      .data(data, function(d) {
        return d[0];
      });

    circles.enter()
      .append("circle");

    circles
      .attr("cx", function(d) {
        return projection([d[1], d[0]])[0];
      })
      .attr("cy", function(d) {        
        return projection([d[1], d[0]])[1];
      })
      .style("opacity", 1)
      .attr("fill", initialFillColor)
      .attr("r", 0)
      .transition()
      .duration(1000)
      .attr("r", circleSmall);

    circles.transition()
      .delay(1000)
      .duration(2000)
      .style("opacity", 0)
      .attr("r", circleLarge)
      .attr('fill', fadeOutFillColor)
      .remove()

    circles.exit()
  }
});
