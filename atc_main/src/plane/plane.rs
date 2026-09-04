use macroquad::math::{Vec2, Vec3};
use macroquad::prelude;

/// Generic struct for a plane, that includes position, callsign, squawk
#[derive(Debug, Clone)]
struct Plane {
    pub callsign: String,
    pub squawk: u16,
    pub pos: Vec3, // lat, lon, alt
    pub velocity: f32,
}

impl Plane {
    /// Spawns a new plane with given lat/lon position. Velocity & altitude are random
    pub fn new(initial_latlon: Vec2) -> Self {
        Self { callsign: callsign, squawk: 1200, pos: }
    }
}
