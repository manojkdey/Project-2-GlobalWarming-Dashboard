function buildMetadata(sample) {
  d3.json(`/metadata/${sample}`).then((data) => {
    // Use d3 to select the panel with id of `#sample-metadata`
    var PANEL = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
    PANEL.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(data).forEach(([key, value]) => {
      PANEL.append("h6").text(`${key}: ${value}`);
    });

    // BONUS: Build the Gauge Chart
    buildGauge(data.WFREQ);
  });
}

function buildCharts(sample) {
  d3.json(`/samples/${sample}`).then((data) => {
    const Year = data.Year;
    const tempAnnamolies = data.tempAnnamolies;
    const sample_values = data.Month;

    // Build a Bubble Chart
    var bubbleLayout = {
      margin: { t: 0 },
      hovermode: "closest",
      xaxis: { title: "Year" }
    };
    var bubbleData = [
      {
        x: Year,
        y: tempAnnamolies,
        text: sample_values,
        mode: "markers",
        marker: {
          size: sample_values,
          color: tempAnnamolies,
          colorscale: "Earth"
        }
      }
    ];

    Plotly.plot("bubble", bubbleData, bubbleLayout);

    // Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
    var pieData = [
      {
        values: tempAnnamolies.slice(0, 20),
        labels: Year.slice(0, 20),
        hovertext: tempAnnamolies.slice(0, 20),
        hoverinfo: "hovertext",
        type: "pie"
      }
    ];

    var pieLayout = {
      margin: { t: 0, l: 0 }
    };

    Plotly.plot("pie", pieData, pieLayout);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
