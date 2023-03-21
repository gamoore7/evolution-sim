use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Species {
    starting_umber: u32,
    size: u32,
    speed: u32,
    sight: u32,
    health: u32,
    cohesion: f32,
    aggression: f32,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SimInput {
    num_timesteps: u32, // Limit 1, 1000
    view_granularity: u32, // Limit 1, 1000
    cache_views: bool,
    world_size_x: u32,
    world_size_y: u32,
    food_density: f32,
    species_list: Vec<Species>,
}

