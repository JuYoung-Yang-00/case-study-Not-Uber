use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufReader, Write};
use serde::Deserialize;
use csv::{ReaderBuilder, WriterBuilder};
use std::time::Instant;

#[derive(Deserialize)]
struct Node {
    lon: f64,
    lat: f64,
}

#[derive(Debug, Deserialize)]
struct EdgeRecord {
    start_id: usize,
    end_id: usize,
    length: f64,
    #[serde(flatten)]
    speed_data: HashMap<String, f64>,
}


fn apsp_runner(_count: usize, nodefile_path: String, edgefile_path: String, outputfile_path: String) -> Result<(), Box<dyn std::error::Error>> {
    
    // Load node data from JSON
    let file = File::open(nodefile_path)?;
    let reader = BufReader::new(file);
    let node_json: HashMap<String, Node> = serde_json::from_reader(reader)?;
    let mut nodes = Vec::new();
    for (k, v) in node_json {
        nodes.push((k, v.lon, v.lat));
    }

    // Load edge data from CSV
    let file = File::open(edgefile_path)?;
    let mut rdr = ReaderBuilder::new().has_headers(true).from_reader(file);
    let mut edges = Vec::new();
    
    for result in rdr.deserialize() {
        let record: EdgeRecord = result?;
        
        let mut cost_weekdays = Vec::new();
        let mut cost_weekends = Vec::new();

        for i in 0..24 {
            let weekday_speed = record.speed_data[&format!("weekday_{}", i)];
            let weekend_speed = record.speed_data[&format!("weekend_{}", i)];
            cost_weekdays.push(record.length / weekday_speed);
            cost_weekends.push(record.length / weekend_speed);
        }

        edges.push((record.start_id, record.end_id, cost_weekdays, cost_weekends));
    }

    println!("data loaded");

    let mut node_id_to_index = HashMap::new();
    for (index, (node_id, _, _)) in nodes.iter().enumerate() {
        node_id_to_index.insert(node_id.parse::<usize>().unwrap(), index);
    }

    // Floyd-Warshall Algorithm
    let vertex_count = nodes.len();
    println!("vertex_count: {}", vertex_count);

    let mut cost_matrix = vec![vec![f64::INFINITY; vertex_count]; vertex_count];
    for i in 0..vertex_count {
        cost_matrix[i][i] = 0.0;
    }
    
    for edge in &edges {
        let (start_id, end_id, _cost_weekdays, _cost_weekends) = edge;

        // Map node IDs to indices
        let _start_idx = *node_id_to_index.get(start_id).unwrap();
        let _end_idx = *node_id_to_index.get(end_id).unwrap();

        // initalize cost matrix
        cost_matrix[_start_idx][_end_idx] = _cost_weekdays[0];

    }

    println!("Floyd-Warshall Algorithm Starting with vertex count {}", vertex_count);

    // start timing
    let start_time = Instant::now();

    for k in 0..vertex_count {

        for i in 0..vertex_count {
            for j in 0..vertex_count {
                let through_k = cost_matrix[i][k] + cost_matrix[k][j];
                if through_k < cost_matrix[i][j] {
                    cost_matrix[i][j] = through_k;
                }
            }
        }

    }


    // measure time taken
    println!("Floyd-Warshall Algorithm Complete");
    let duration = start_time.elapsed();
    println!("node count {}, duration: {:.2?}", vertex_count, duration);

    // Save the shortest path costs to CSV
    let file = File::create(outputfile_path)?;
    let mut wtr = WriterBuilder::new().from_writer(file);

    let headers: Vec<String> = (0..vertex_count).map(|i| i.to_string()).collect();
    
    // Here, we create a new iterator chain and pass it directly without a reference
    wtr.write_record(["Node"].into_iter().chain(headers.iter().map(String::as_str)))?;

    for i in 0..vertex_count {
        let row: Vec<String> = cost_matrix[i].iter().map(|x| x.to_string()).collect();

        // Similarly, create a new iterator chain here
        wtr.write_record(std::iter::once(i.to_string().as_str()).chain(row.iter().map(String::as_str)))?;
    }

    wtr.flush()?;

    Ok(())

}

fn main() -> io::Result<()> {

    // for 1000, 2000, ..., 10000
    for count in (1..=10).map(|x| x * 1000) {

        let nodefile_path = format!("../../data/modified_node_data_{}.json", count);
        let edgefile_path = format!("../../data/modified_edges_{}.csv", count);
        let outputfile_path = format!("./data/shortest_path_costs_{}.csv.csv", count);

        apsp_runner(count, nodefile_path, edgefile_path, outputfile_path).unwrap();

    }

    Ok(())
}
