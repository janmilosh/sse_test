$(function() {

  var width = 1000,
      height = 600,
      circleSmall,
      circleLarge,
      pathWidth = 0.25,
      initialFillColor = 'red',
      fadeOutFillColor = 'pink'

  function setSizes() {
    var windowHeight = $(window).height();
    var windowWidth = $(window).width();
    if (windowWidth >= 1024) {
      width = windowWidth * 0.9;
    } else {
      width = 1000;
    }
    height = width * 0.6;
    circleSmall = 3 * width/1000;
    circleLarge = circleSmall;
    strokeWidth = 1;

    $('#usa-map').css({'height': height + 'px',
                       'width': width + 'px',
                       'margin-left': 'auto',
                       'margin-right': 'auto',
                       'margin-top': ((windowHeight-height)/2) + 'px'
                     });
  }

  setSizes();

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

  group.on('click', function() {
    var point = d3.mouse(this),
        p = {x: point[0], y: point[1] };

    // Append a new point
    circle = group.append("circle")
      .attr("transform", "translate(" + p.x + "," + p.y + ")")
      .attr("r", "8")
      .attr("class", "circle");

    circle.transition()
      .delay(1000)
      .duration(2000)
      .style("opacity", 0)
      .attr("r", circleLarge)
      .attr('fill', fadeOutFillColor)
      .remove();

    var latlonArray = projection.invert(d3.mouse(this));

    clickData = {"lat": latlonArray[1], "lon": latlonArray[0]}
    var sendData = d3.xhr('/publish');

    sendData.header("Content-Type", "application/json")
      .post(JSON.stringify(clickData), function(error,received) {
        console.log('error', error);
        console.log('received', received);
    });
  });
});
