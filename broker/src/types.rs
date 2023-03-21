use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Species {
    starting_umber: u8,
    size: u8,
    speed: u8,
    sight: u8,
    health: u8,
    cohesion: u8,
    aggression: u8,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SimInput {
    num_timesteps: u16, // Limit 1, 1000
    view_granularity: u16, // Limit 1, 1000
    cache_views: u16,
    world_size_x: u8,
    world_size_y: u8,
    food_density: u32,
    species_list: Vec<Species>,
}

